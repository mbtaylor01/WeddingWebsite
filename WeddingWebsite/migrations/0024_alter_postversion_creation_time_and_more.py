# Generated by Django 4.2.2 on 2023-08-23 04:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('WeddingWebsite', '0023_post_edited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postversion',
            name='creation_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='thread',
            name='creation_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
