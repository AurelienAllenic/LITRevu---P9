# Generated by Django 5.0.1 on 2024-02-08 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangoApp', '0009_rename_descriptionreview_review_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='image',
        ),
    ]
