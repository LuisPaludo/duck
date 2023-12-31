# Generated by Django 4.2.4 on 2023-08-23 05:24

from django.db import migrations, models
import user_data.models


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0005_prizes_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prizes',
            name='logo',
            field=models.ImageField(blank=True, default='users_photos/default.png', max_length=500, null=True, upload_to='logos', validators=[user_data.models.validate_image_size]),
        ),
    ]
