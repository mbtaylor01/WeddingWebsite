from datetime import datetime
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

class RSVP(models.Model):
    full_name = models.CharField(max_length=100)
    additional_people = models.IntegerField()
    allergies = models.CharField(max_length=1000)
    alcohol = models.CharField(max_length=1000)
    other = models.CharField(max_length=5000)

class RegistryEntry(models.Model):
    title = models.CharField(max_length=500)
    image = models.ImageField(upload_to="images")
    image_link = models.URLField()
    reserved_by = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

class Thread(models.Model):
    title = models.CharField(max_length=500)
    creator = models.CharField(max_length=100)
    creation_time = models.DateTimeField(default=datetime.now, blank=True)
    slug = models.SlugField(default="")

    def get_absolute_url(self):
        return reverse("thread", kwargs={
            "threadslug": slugify(self.title),
            })
    
    def __str__(self):
        return self.title
    
class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to="profile_pics", default="profile_pics/default/default.png")

    def get_absolute_url(self):
        return reverse("change-profile-pic")
    
class Post(models.Model):
    text = models.TextField()
    creator = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(default=datetime.now, blank=True)


