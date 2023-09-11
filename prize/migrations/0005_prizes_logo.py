# Generated by Django 4.2.4 on 2023-08-23 05:19

from django.db import migrations, models
import user_data.models


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0004_prizecategory_remove_prizes_used_by_prizes_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='prizes',
            name='logo',
            field=models.ImageField(blank=True, default='assets/users_photos/default.png', max_length=500, null=True, upload_to='logos', validators=[user_data.models.validate_image_size]),
        ),
    ]