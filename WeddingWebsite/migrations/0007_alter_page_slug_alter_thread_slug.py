# Generated by Django 4.2.2 on 2023-06-29 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeddingWebsite', '0006_page_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(default=''),
        ),
        migrations.AlterField(
            model_name='thread',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
