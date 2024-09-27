from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import ChangeRequest, Asset, EmployeeAsset, UpdateAsset, AddAsset, ReplaceAsset


@receiver(post_save, sender=ChangeRequest)
def handle_change_request_approval(sender, instance, **kwargs):
    if instance.status == 'APP':  # Only proceed if the status is 'Approved'
        try:
            with transaction.atomic():
                if instance.type == 'UPD':
                    handle_update_asset(instance)
                elif instance.type == 'ADD':
                    handle_add_asset(instance)
                elif instance.type == 'REP':
                    handle_replace_asset(instance)
        except ValidationError as e:
            # If a ValidationError occurs, revert the status to 'Pending'
            instance.status = 'PEN'
            instance.save()
            raise e


def handle_update_asset(change_request):
    update_asset = UpdateAsset.objects.get(change_request=change_request)
    asset = update_asset.asset

    # Update the asset with the new meta_data
    asset.meta_data = update_asset.meta_data
    asset.save()


def handle_add_asset(change_request):
    add_asset = AddAsset.objects.get(change_request=change_request)
    asset = add_asset.asset

    # Check if the asset is already assigned to an employee
    if EmployeeAsset.objects.filter(asset=asset, to_date__isnull=True).exists():
        raise ValidationError("Cannot add an asset that is already assigned to an employee.")

    # Update the status of AddAsset to 'Completed'
    add_asset.status = 'COM'
    add_asset.save()


def handle_replace_asset(change_request):
    replace_asset = ReplaceAsset.objects.get(change_request=change_request)
    from_asset = replace_asset.from_asset
    to_asset = replace_asset.to_asset

    # Check if the 'from_asset' is assigned to an employee
    employee_asset = EmployeeAsset.objects.filter(asset=from_asset, to_date__isnull=True).first()
    if not employee_asset:
        raise ValidationError("The asset to be replaced is not currently assigned to any employee.")

    # Check if the 'to_asset' is already assigned to an employee
    if EmployeeAsset.objects.filter(asset=to_asset, to_date__isnull=True).exists():
        raise ValidationError("The new asset is already assigned to an employee.")

    # Update the existing EmployeeAsset record
    employee_asset.to_date = replace_asset.from_date
    employee_asset.save()

    # Create a new EmployeeAsset record for the new asset
    EmployeeAsset.objects.create(
        asset=to_asset,
        employee=employee_asset.employee,
        from_date=replace_asset.from_date,
        to_date=replace_asset.to_date
    )

    # Update the meta_data of the new asset
    to_asset.meta_data = replace_asset.meta_data
    to_asset.save()