# Generated by Django 3.2.4 on 2021-06-15 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_shop'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shop',
            old_name='owner',
            new_name='user',
        ),
    ]
