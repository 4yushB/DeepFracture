# Generated by Django 3.2.12 on 2022-05-27 08:38

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('cam_app2', '0004_delete_imagepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('name_title', models.CharField(blank=True, max_length=100, null=True)),
                ('name_subtitle', wagtail.core.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
