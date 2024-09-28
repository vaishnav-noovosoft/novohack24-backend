# serializers.py
from rest_framework import serializers
from .models import Asset, EmployeeAsset, ChangeRequest, UpdateAsset, AddAsset, ReplaceAsset


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'type', 'meta_data', 'serial_no']


class EmployeeAssetSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(read_only=True)

    class Meta:
        model = EmployeeAsset
        fields = ['id', 'asset', 'employee', 'from_date', 'to_date']


class AddAssetSerializer(serializers.Serializer):
    asset = serializers.PrimaryKeyRelatedField(queryset=Asset.objects.filter(employee_asset__isnull=True))

