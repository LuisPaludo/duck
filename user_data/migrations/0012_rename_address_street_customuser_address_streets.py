# Generated by Django 4.2.4 on 2023-09-08 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_data', '0011_rename_addres_rua_customuser_address_city_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='address_street',
            new_name='address_streets',
        ),
    ]
