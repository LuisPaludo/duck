# Generated by Django 4.2.4 on 2023-08-21 06:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prizes',
            name='cost_in_points',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
