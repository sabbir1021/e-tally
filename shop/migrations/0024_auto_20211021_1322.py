# Generated by Django 3.2.8 on 2021-10-21 07:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_auto_20210622_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cash',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 21, 13, 22, 0, 756662)),
        ),
        migrations.AlterField(
            model_name='customer_cost_pay',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 21, 13, 22, 0, 754801)),
        ),
    ]
