# Generated by Django 3.2.4 on 2021-06-21 19:11

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0013_rename_supplierr_cost_supplier_cost'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Supplier_Cost',
            new_name='Supplier_Buy_Pay',
        ),
    ]
