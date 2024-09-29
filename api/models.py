from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import QuerySet
from django.utils import timezone


class Seat(models.Model):
    id = models.AutoField(primary_key=True)


class User(AbstractUser):
    role = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)


class Asset(models.Model):
    TYPE_CHOICES = [
        ('HW', 'Hardware'),
        ('SW', 'Software'),
        ('OTH', 'Other'),
    ]

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    meta_data = models.JSONField(null=True, blank=True)
    serial_no = models.CharField(unique=True)

    # related names
    employee_asset: "EmployeeAsset"


class EmployeeAsset(models.Model):
    id = models.AutoField(primary_key=True)
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name="employee_asset")
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)


class ChangeRequest(models.Model):
    TYPE_CHOICES = [
        ('ADD', 'Add'),
        ('UPD', 'Update'),
        ('REP', 'Replace'),
    ]
    STATUS_CHOICES = [
        ('PEN', 'Pending'),
        ('APP', 'Approved'),
        ('REJ', 'Rejected'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default="PEN")


class UpdateAsset(models.Model):
    id = models.AutoField(primary_key=True)
    change_request = models.ForeignKey(ChangeRequest, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    meta_data = models.JSONField(null=True, blank=True)


class AddAsset(models.Model):
    id = models.AutoField(primary_key=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    change_request = models.ForeignKey(ChangeRequest, on_delete=models.CASCADE)


class ReplaceAsset(models.Model):
    id = models.AutoField(primary_key=True)
    from_asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='replaced_from')
    to_asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='replaced_to')
    change_request = models.ForeignKey(ChangeRequest, on_delete=models.CASCADE)

