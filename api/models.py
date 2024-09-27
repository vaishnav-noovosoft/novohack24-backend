from django.db import models
from django.contrib.auth.models import AbstractUser
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
    serial_no = models.IntegerField()


class EmployeeAsset(models.Model):
    id = models.AutoField(primary_key=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()


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
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    meta_data = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)


class UpdateAsset(models.Model):
    id = models.AutoField(primary_key=True)
    change_request = models.ForeignKey(ChangeRequest, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    meta_data = models.JSONField(null=True, blank=True)


class AddAsset(models.Model):
    STATUS_CHOICES = [
        ('PEN', 'Pending'),
        ('COM', 'Completed'),
        ('CAN', 'Cancelled'),
    ]

    id = models.AutoField(primary_key=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    change_request = models.ForeignKey(ChangeRequest, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)


class ReplaceAsset(models.Model):
    id = models.AutoField(primary_key=True)
    from_asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='replaced_from')
    to_asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='replaced_to')
    meta_data = models.JSONField(null=True, blank=True)
    change_request = models.ForeignKey(ChangeRequest, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()