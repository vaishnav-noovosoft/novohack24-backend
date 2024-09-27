from rest_framework import viewsets
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


class ChangeRequestViewSet(viewsets.ModelViewSet):
    queryset = ChangeRequest.objects.all()
    serializer_class = ChangeRequestSerializer

    def create(self, request, *args, **kwargs):
        pass


class UpdateAssetViewSet(viewsets.ModelViewSet):
    queryset = UpdateAsset.objects.all()
    serializer_class = UpdateAssetSerializer


class AddAssetViewSet(viewsets.ModelViewSet):
    queryset = AddAsset.objects.all()
    serializer_class = AddAssetSerializer


class ReplaceAssetViewSet(viewsets.ModelViewSet):
    queryset = ReplaceAsset.objects.all()
    serializer_class = ReplaceAssetSerializer
