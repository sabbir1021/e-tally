# Generated by Django 3.2.4 on 2021-06-22 11:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_alter_cash_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cash',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 22, 17, 31, 27, 617405)),
        ),
        migrations.AlterField(
            model_name='customer_cost_pay',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 22, 17, 31, 27, 615367)),
        ),
    ]
