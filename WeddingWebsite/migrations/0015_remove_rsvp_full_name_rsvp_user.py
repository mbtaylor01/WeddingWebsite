# Generated by Django 4.2.2 on 2023-08-01 02:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WeddingWebsite', '0014_alter_rsvp_additional_people_alter_rsvp_alcohol_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rsvp',
            name='full_name',
        ),
        migrations.AddField(
            model_name='rsvp',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
