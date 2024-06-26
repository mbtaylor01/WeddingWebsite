from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser


class RSVP(models.Model):
    """
    Model for an RSVP each user fills out.
    """
    party_size = models.PositiveSmallIntegerField()
    allergies = models.CharField(max_length=1000, blank=True)
    alcohol = models.CharField(max_length=1000, blank=True)
    other = models.TextField(max_length=5000, blank=True)

    def __str__(self):
        return f"{self.party_size}"
        

class CustomUser(AbstractUser):
    """
    A normal user object, but with profile_pic and rsvp added.
    """
    profile_pic = models.ImageField(upload_to="profile_pics", default="profile_pics/default/default.png")
    rsvp = models.OneToOneField(RSVP, on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("account-info")


class RegistryEntry(models.Model):
    """
    Model for an item in the registry.
    """
    title = models.CharField(max_length=500)
    image = models.ImageField(upload_to="images")
    # users can click the image to go to the website where the item is sold
    image_link = models.URLField()
    # users can reserve an item
    reserved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    # certain items like honeymoon donations should not be reservable
    is_reservable = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Thread(models.Model):
    """
    Model for a thread in the forum.
    """
    title = models.CharField(max_length=500)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(default=timezone.now, blank=True)
    # default slug has max_length 50 and if title exceeds 50 a 500 error is thrown
    slug = models.SlugField(max_length=500, default="")

    def get_absolute_url(self):
        return reverse("thread", kwargs={
            "threadslug": slugify(self.title),
            })
    
    def __str__(self):
        return self.title


class Post(models.Model):
    """
    Model for a post in a thread.
    """
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    # if a post is edited, "(edited)" will display at the end
    edited = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class PostVersion(models.Model):
    """
    Model for a version of an individual post  Only the most recent version is displayed.
    """
    text = models.TextField()
    creation_time = models.DateTimeField(default=timezone.now, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    
    class Meta:
        # set ordering so post.postversion_set.last.text in template always gets most recent post
        ordering = ("creation_time",)