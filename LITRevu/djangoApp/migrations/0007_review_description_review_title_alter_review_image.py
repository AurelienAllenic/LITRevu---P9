# Generated by Django 5.0.1 on 2024-02-02 14:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoApp', '0006_remove_review_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='reviews/'),
        ),
    ]
