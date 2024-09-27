# serializers.py
from rest_framework import serializers
from .models import Asset, EmployeeAsset, ChangeRequest, UpdateAsset, AddAsset, ReplaceAsset


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'type', 'meta_data', 'serial_no']


class EmployeeAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAsset
        fields = ['id', 'asset', 'employee', 'from_date', 'to_date']


class ChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeRequest
        fields = ['id', 'user', 'asset', 'type', 'meta_data', 'status']


class ChangeRequestDetailsSerializer(serializers.ModelSerializer):
    asset = AssetSerializer()

    class Meta:
        model = ChangeRequest
        fields = ['id', 'user', 'asset', 'type', 'meta_data', 'status']


class UpdateAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpdateAsset
        fields = '__all__'


class UpdateAssetDetailsSerializer(serializers.ModelSerializer):
    asset = AssetSerializer()

    class Meta:
        model = UpdateAsset
        fields = '__all__'


class AddAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddAsset
        fields = ['id', 'asset', 'change_request', 'status']


class AddAssetDetailsSerializer(serializers.ModelSerializer):
    asset = AssetSerializer()

    class Meta:
        model = AddAsset
        fields = '__all__'


class ReplaceAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplaceAsset
        fields = ['id', 'from_asset', 'to_asset', 'meta_data', 'change_request', 'from_date', 'to_date']


class ReplaceAssetDetailsSerializer(serializers.ModelSerializer):
    from_asset = AssetSerializer()
    to_asset = AssetSerializer()

    class Meta:
        model = ReplaceAsset
        fields = '__all__'
