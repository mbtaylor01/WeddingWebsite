# Generated by Django 4.2.2 on 2023-08-01 23:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WeddingWebsite', '0017_alter_customuser_rsvp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='rsvp',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='WeddingWebsite.rsvp'),
        ),
    ]
