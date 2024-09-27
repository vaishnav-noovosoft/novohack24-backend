from rest_framework.response import Response
from rest_framework import viewsets

from .models import Asset, EmployeeAsset, UpdateAsset, AddAsset, ReplaceAsset, ChangeRequest
from .serializers import (
    AssetSerializer, EmployeeAssetSerializer, UpdateAssetSerializer, AddAssetSerializer, ReplaceAssetSerializer,ChangeRequestSerializer
)


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class EmployeeAssetViewSet(viewsets.ModelViewSet):
    queryset = EmployeeAsset.objects.all()
    serializer_class = EmployeeAssetSerializer


class ChangeRequestViewSet(viewsets.ModelViewSet):
    queryset = ChangeRequest.objects.all()
    serializer_class = ChangeRequestSerializer  # Specify the serializer class

    def list(self, request):
        queryset = self.queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class UpdateAssetViewSet(viewsets.ModelViewSet):
    queryset = UpdateAsset.objects.all()
    serializer_class = UpdateAssetSerializer


class AddAssetViewSet(viewsets.ModelViewSet):
    queryset = AddAsset.objects.all()
    serializer_class = AddAssetSerializer


class ReplaceAssetViewSet(viewsets.ModelViewSet):
    queryset = ReplaceAsset.objects.all()
    serializer_class = ReplaceAssetSerializer
