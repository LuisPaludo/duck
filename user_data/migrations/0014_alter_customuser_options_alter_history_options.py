# Generated by Django 4.2.4 on 2023-09-09 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_data', '0013_rename_address_streets_customuser_address_street'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name_plural': 'Users'},
        ),
        migrations.AlterModelOptions(
            name='history',
            options={'verbose_name_plural': 'Users History'},
        ),
    ]
