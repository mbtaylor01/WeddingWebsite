from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class RSVP(models.Model):
    party_size = models.PositiveSmallIntegerField(null=True, blank=True)
    allergies = models.CharField(max_length=1000, blank=True)
    alcohol = models.CharField(max_length=1000, blank=True)
    other = models.TextField(max_length=5000, blank=True)

    def __str__(self):
        return f"{self.party_size}"
        

class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to="profile_pics", default="profile_pics/default/default.png")
    rsvp = models.OneToOneField(RSVP, on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("change-profile-pic")

class RegistryEntry(models.Model):
    title = models.CharField(max_length=500)
    image = models.ImageField(upload_to="images")
    image_link = models.URLField()
    reserved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class Thread(models.Model):
    title = models.CharField(max_length=500)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(default=timezone.now, blank=True)
    slug = models.SlugField(default="")

    def get_absolute_url(self):
        return reverse("thread", kwargs={
            "threadslug": slugify(self.title),
            })
    
    def __str__(self):
        return self.title
    
class Post(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class PostVersion(models.Model):
    text = models.TextField()
    creation_time = models.DateTimeField(default=timezone.now, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    
    class Meta:
        # set ordering so post.postversion_set.last.text in template always gets most recent post
        ordering = ("creation_time",)