# Generated by Django 4.2.4 on 2023-08-23 07:00

import django.core.validators
from django.db import migrations, models
import prize.models


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0006_alter_prizes_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='redeemedprizes',
            name='qr_code',
            field=models.URLField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='prizes',
            name='code',
            field=models.CharField(default=prize.models.generate_random_code, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='prizes',
            name='times_to_be_used',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='prizes',
            name='times_used',
            field=models.IntegerField(default=0),
        ),
    ]
