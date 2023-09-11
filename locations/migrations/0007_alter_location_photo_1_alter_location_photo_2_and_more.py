# Generated by Django 4.2.4 on 2023-09-11 18:48

from django.db import migrations, models
import locations.models
import user_data.models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0006_alter_touristattraction_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='photo_1',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to=locations.models.get_upload_path_locations, validators=[user_data.models.validate_image_size]),
        ),
        migrations.AlterField(
            model_name='location',
            name='photo_2',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to=locations.models.get_upload_path_locations, validators=[user_data.models.validate_image_size]),
        ),
        migrations.AlterField(
            model_name='location',
            name='photo_3',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to=locations.models.get_upload_path_locations, validators=[user_data.models.validate_image_size]),
        ),
        migrations.AlterField(
            model_name='location',
            name='photo_4',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to=locations.models.get_upload_path_locations, validators=[user_data.models.validate_image_size]),
        ),
        migrations.AlterField(
            model_name='touristattraction',
            name='photo',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to=locations.models.get_upload_path_attractions, validators=[user_data.models.validate_image_size]),
        ),
    ]