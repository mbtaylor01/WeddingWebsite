# Generated by Django 4.2.2 on 2023-06-30 04:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('WeddingWebsite', '0007_alter_page_slug_alter_thread_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='page',
        ),
        migrations.AddField(
            model_name='post',
            name='creation_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Page',
        ),
    ]
