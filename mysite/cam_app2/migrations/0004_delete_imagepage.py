# Generated by Django 3.2.12 on 2022-05-27 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailcore', '0066_collection_management_permissions'),
        ('cam_app2', '0003_imagepage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ImagePage',
        ),
    ]
