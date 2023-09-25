# Generated by Django 4.2.4 on 2023-09-21 19:35

from django.db import migrations, models
import locations.models
import user_data.models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0007_alter_location_photo_1_alter_location_photo_2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='photo_1',
            field=models.ImageField(blank=True, max_length=1000, null=True, upload_to=locations.models.get_upload_path_locations, validators=[user_data.models.validate_image_size]),
        ),
        migrations.AlterField(
            model_name='location',
            name='photo_2',
            field=models.ImageField(blank=True, max_length=1000, null=True, upload_to=locations.models.get_upload_path_locations, validators=[user_data.models.validate_image_size]),
        ),
        migrations.AlterField(
            model_name='location',
            name='photo_3',
            field=models.ImageField(blank=True, max_length=1000, null=True, upload_to=locations.models.get_upload_path_locations, validators=[user_data.models.validate_image_size]),
        ),
        migrations.AlterField(
            model_name='location',
            name='photo_4',
            field=models.ImageField(blank=True, max_length=1000, null=True, upload_to=locations.models.get_upload_path_locations, validators=[user_data.models.validate_image_size]),
        ),
        migrations.AlterField(
            model_name='location',
            name='slug_field',
            field=models.SlugField(blank=True, default='', max_length=100, null=True),
        ),
    ]