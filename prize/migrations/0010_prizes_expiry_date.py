# Generated by Django 4.2.4 on 2023-08-26 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0009_alter_redeemedprizes_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='prizes',
            name='expiry_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
