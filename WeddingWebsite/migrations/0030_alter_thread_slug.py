# Generated by Django 4.2.2 on 2024-02-09 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeddingWebsite', '0029_registryentry_is_reservable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='slug',
            field=models.SlugField(default='', max_length=500),
        ),
    ]
