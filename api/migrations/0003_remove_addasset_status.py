# Generated by Django 5.1.1 on 2024-09-27 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_asset_serial_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addasset',
            name='status',
        ),
    ]
