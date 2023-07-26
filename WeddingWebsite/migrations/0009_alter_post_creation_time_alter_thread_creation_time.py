# Generated by Django 4.2.2 on 2023-06-30 05:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeddingWebsite', '0008_remove_post_page_post_creation_time_delete_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='creation_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='thread',
            name='creation_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
