# Generated by Django 4.2.2 on 2024-02-07 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeddingWebsite', '0028_alter_rsvp_party_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='registryentry',
            name='is_reservable',
            field=models.BooleanField(default=True),
        ),
    ]
