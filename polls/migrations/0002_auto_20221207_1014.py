# Generated by Django 3.2.16 on 2022-12-07 10:14

import django.core.validators
from django.db import migrations, models
import polls.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='full_description',
            field=models.CharField(blank=True, max_length=250, verbose_name='Полное описание'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_image',
            field=models.ImageField(blank=True, upload_to=polls.models.get_name_file, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp']), polls.models.validate_image_size]),
        ),
        migrations.AddField(
            model_name='question',
            name='short_description',
            field=models.CharField(blank=True, max_length=100, verbose_name='Краткое описание'),
        ),
    ]