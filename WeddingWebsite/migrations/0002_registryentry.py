# Generated by Django 4.2.2 on 2023-06-28 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeddingWebsite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistryEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('image', models.ImageField(upload_to='images')),
                ('image_link', models.URLField()),
                ('reserved_by', models.CharField(max_length=500)),
            ],
        ),
    ]
