from rest_framework import viewsets
from .models import Asset, EmployeeAsset, ChangeRequest, UpdateAsset, AddAsset, ReplaceAsset
from .serializers import (
    AssetSerializer, EmployeeAssetSerializer, ChangeRequestSerializer,
    UpdateAssetSerializer, AddAssetSerializer, ReplaceAssetSerializer
)


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class EmployeeAssetViewSet(viewsets.ModelViewSet):
    queryset = EmployeeAsset.objects.all()
    serializer_class = EmployeeAssetSerializer


class ChangeRequestViewSet(viewsets.ModelViewSet):
    queryset = ChangeRequest.objects.all()
    serializer_class = ChangeRequestSerializer


class UpdateAssetViewSet(viewsets.ModelViewSet):
    queryset = UpdateAsset.objects.all()
    serializer_class = UpdateAssetSerializer


class AddAssetViewSet(viewsets.ModelViewSet):
    queryset = AddAsset.objects.all()
    serializer_class = AddAssetSerializer


class ReplaceAssetViewSet(viewsets.ModelViewSet):
    queryset = ReplaceAsset.objects.all()
    serializer_class = ReplaceAssetSerializer
