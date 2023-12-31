# Generated by Django 4.2.4 on 2023-08-20 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prize', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prizes',
            name='generated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='generated_prizes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='prizes',
            name='used_by',
            field=models.ManyToManyField(blank=True, related_name='used_prizes', to=settings.AUTH_USER_MODEL),
        ),
    ]
