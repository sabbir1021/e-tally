# Generated by Django 3.2.4 on 2021-06-21 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_delete_shop'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cash',
            name='pay_cash',
        ),
    ]
