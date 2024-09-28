from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .models import Asset, EmployeeAsset, ChangeRequest, ReplaceAsset, AddAsset
from .serializers import (
    AssetSerializer, EmployeeAssetSerializer, AddAssetSerializer, ReplaceAssetSerializer
)


class AssetFilter(filters.FilterSet):
    type = filters.CharFilter(lookup_expr="icontains")
    serial_no = filters.CharFilter(lookup_expr="icontains")
    meta_data = filters.CharFilter(field_name="meta_data", method="filter_meta_data")

    def filter_meta_data(self, queryset, name, value):
        return queryset.filter(meta_data__contains=value)

    class Meta:
        model = Asset
        fields = ["id", "type", "meta_data", "serial_no"]


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    filterset_class = AssetFilter
    filter_backends = (filters.DjangoFilterBackend,)


class EmployeeAssetViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = EmployeeAsset.objects.all()
    serializer_class = EmployeeAssetSerializer

    def get_queryset(self):
        if self.request.user.role == "admin":
            return self.queryset.all().select_related("asset")

        return self.queryset.filter(employee=self.request.user).select_related("asset")


class AddAssetViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ChangeRequest.objects.filter(type="ADD")
    serializer_class = AddAssetSerializer

    def create(self, request, *args, **kwargs):
        add_asset_serializer = AddAssetSerializer(data=request.data)
        add_asset_serializer.is_valid(raise_exception=True)

        asset: Asset = add_asset_serializer.validated_data.get("asset")

        # Create a ChangeRequest for adding an asset
        change_request_data = {
            "user": request.user,
            "asset": asset,
            "type": "ADD",
            "status": "PEN",
        }
        change_request = ChangeRequest.objects.create(data=change_request_data)

        # Create an AddAsset instance linked to the ChangeRequest
        add_asset_data = {
            "asset": asset,
            "change_request": change_request,
        }
        AddAsset.objects.create(data=add_asset_data)

        return Response(change_request, status=status.HTTP_201_CREATED)


class ReplaceAssetViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ChangeRequest.objects.filter(type='REP')
    serializer_class = ReplaceAssetSerializer

    def create(self, request, *args, **kwargs):
        replace_asset_serializer = ReplaceAssetSerializer(data=request.data)
        replace_asset_serializer.is_valid(raise_exception=True)

        from_asset: Asset = replace_asset_serializer.validated_data.get("from_asset")
        if not from_asset.employee_asset.employee == self.request.user:
            return Response({"error": "from_asset does not belong to you"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a ChangeRequest for replacing an asset
        change_request_data = {
            "user": request.user,
            "asset": from_asset,
            "type": "REP",
            "status": "PEN"  # Set initial status as Pending
        }
        change_request = ChangeRequest.objects.create(data=change_request_data)

        # Create a ReplaceAsset instance linked to the ChangeRequest
        replace_asset_data = {
            "from_asset": request.data.get("from_asset"),
            "to_asset": request.data.get("to_asset"),
            "change_request": change_request,
        }
        ReplaceAsset.objects.create(data=replace_asset_data)

        return Response(change_request, status=status.HTTP_201_CREATED)
