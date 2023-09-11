# Generated by Django 4.2.4 on 2023-09-06 07:48

import django.core.validators
from django.db import migrations, models
import prize.models


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0013_prizes_disabled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prizes',
            name='discount_value',
        ),
        migrations.AlterField(
            model_name='prizes',
            name='cost_in_points',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(1000)]),
        ),
        migrations.AlterField(
            model_name='prizes',
            name='expiry_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='prizes',
            name='times_to_be_used',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3000)]),
        ),
    ]