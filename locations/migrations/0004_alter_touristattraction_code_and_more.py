# Generated by Django 4.2.4 on 2023-09-08 23:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_touristattraction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='touristattraction',
            name='code',
            field=models.IntegerField(blank=True, null=True, unique=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='touristattraction',
            name='qr_code',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]