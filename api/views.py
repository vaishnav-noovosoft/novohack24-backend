from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .models import Asset, EmployeeAsset, ChangeRequest, UpdateAsset, AddAsset, ReplaceAsset
from .serializers import (
    AssetSerializer, EmployeeAssetSerializer, ChangeRequestSerializer,
    UpdateAssetSerializer, AddAssetSerializer, ReplaceAssetSerializer
)


class AssetFilter(filters.FilterSet):
    type = filters.CharFilter(lookup_expr='icontains')
    serial_no = filters.CharFilter(lookup_expr='icontains')
    meta_data = filters.CharFilter(field_name='meta_data', method='filter_meta_data')

    def filter_meta_data(self, queryset, name, value):
        return queryset.filter(meta_data__contains=value)

    class Meta:
        model = Asset
        fields = ['id', 'type', 'meta_data', 'serial_no']


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    filterset_class = AssetFilter
    filter_backends = (filters.DjangoFilterBackend,)


class EmployeeAssetViewSet(viewsets.ModelViewSet):
    queryset = EmployeeAsset.objects.all()
    serializer_class = EmployeeAssetSerializer

    def get_queryset(self):
        return self.queryset.filter(employee=self.request.user).select_related("asset")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UpdateAssetViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ChangeRequest.objects.filter(type='UPD')
    serializer_class = ChangeRequestSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Create a ChangeRequest for updating an asset
        change_request_data = {
            'user': request.user.id,
            'asset': request.data.get('asset'),
            'type': 'UPD',
            'meta_data': request.data.get('meta_data'),
            'status': 'PEN'  # Set initial status as Pending
        }
        change_request_serializer = self.get_serializer(data=change_request_data)
        change_request_serializer.is_valid(raise_exception=True)
        change_request = change_request_serializer.save()

        # Create an UpdateAsset instance linked to the ChangeRequest
        update_asset_data = {
            'change_request': change_request.id,
            'asset': request.data.get('asset'),
            'meta_data': request.data.get('meta_data')
        }
        update_asset_serializer = UpdateAssetSerializer(data=update_asset_data)
        update_asset_serializer.is_valid(raise_exception=True)
        update_asset_serializer.save()

        return Response(change_request_serializer.data, status=status.HTTP_201_CREATED)


class AddAssetViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ChangeRequest.objects.filter(type='ADD')
    serializer_class = ChangeRequestSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Create a ChangeRequest for adding an asset
        change_request_data = {
            'user': request.user.id,
            'asset': request.data.get('asset'),
            'type': 'ADD',
            'meta_data': request.data.get('meta_data'),
            'status': 'PEN'  # Set initial status as Pending
        }
        change_request_serializer = self.get_serializer(data=change_request_data)
        change_request_serializer.is_valid(raise_exception=True)
        change_request = change_request_serializer.save()

        # Create an AddAsset instance linked to the ChangeRequest
        add_asset_data = {
            'asset': request.data.get('asset'),
            'change_request': change_request.id,
        }
        add_asset_serializer = AddAssetSerializer(data=add_asset_data)
        add_asset_serializer.is_valid(raise_exception=True)
        add_asset_serializer.save()

        return Response(change_request_serializer.data, status=status.HTTP_201_CREATED)


class ReplaceAssetViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ChangeRequest.objects.filter(type='REP')
    serializer_class = ChangeRequestSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Create a ChangeRequest for replacing an asset
        change_request_data = {
            'user': request.user.id,
            'asset': request.data.get('from_asset'),
            'type': 'REP',
            'meta_data': request.data.get('meta_data'),
            'status': 'PEN'  # Set initial status as Pending
        }
        change_request_serializer = self.get_serializer(data=change_request_data)
        change_request_serializer.is_valid(raise_exception=True)
        change_request = change_request_serializer.save()

        # Create a ReplaceAsset instance linked to the ChangeRequest
        replace_asset_data = {
            'from_asset': request.data.get('from_asset'),
            'to_asset': request.data.get('to_asset'),
            'meta_data': request.data.get('meta_data'),
            'change_request': change_request.id,
            'from_date': request.data.get('from_date'),
            'to_date': request.data.get('to_date')
        }
        replace_asset_serializer = ReplaceAssetSerializer(data=replace_asset_data)
        replace_asset_serializer.is_valid(raise_exception=True)
        replace_asset_serializer.save()

        return Response(change_request_serializer.data, status=status.HTTP_201_CREATED)
