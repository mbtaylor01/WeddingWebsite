from django.contrib import admin
from .models import RSVP, RegistryEntry, Thread, Post, CustomUser, PostVersion
from django.contrib.auth.admin import UserAdmin


class PostAdmin(admin.ModelAdmin): 
    list_filter = ("id", "creator", "thread",)
    list_display = ("id", "most_recent_version", "total_versions", "most_recent_creation_time", "creator", "thread")

    def most_recent_version(self, instance):
        postversions = instance.postversion_set
        return postversions.last().text

    def most_recent_creation_time(self, instance):
        postversions = instance.postversion_set
        return postversions.last().creation_time
    
    def total_versions(self, instance):
        postversions = instance.postversion_set
        return postversions.count()
        
class PostVersionAdmin(admin.ModelAdmin): 
    list_filter = ("creation_time", "post")
    list_display = ("text", "creation_time", "post", "thread")

    def thread(self, instance):
        return instance.post.thread

class RegistryAdmin(admin.ModelAdmin): 
    list_filter = ("title", "reserved_by")
    list_display = ("title", "reserved_by")

class RSVPAdmin(admin.ModelAdmin): 
    list_filter = ("party_size", "allergies", "alcohol", "other")
    list_display = ("user", "party_size", "allergies", "alcohol", "other")

    def user(self, instance):
        # display one-to-one linked customuser.username field in Admin panel
        try:
            return instance.customuser.username
        except RSVP.customuser.RelatedObjectDoesNotExist:
            pass

class ThreadAdmin(admin.ModelAdmin): 
    list_filter = ("creator", "creation_time",)
    list_display = ("title", "total_posts", "creator", "creation_time",)

    def total_posts(self, instance):
        posts = instance.post_set
        return posts.count()


fields = list(UserAdmin.fieldsets)
fields[0] = (None, {'fields': ('username', 'password', 'profile_pic', 'rsvp')})
UserAdmin.fieldsets = tuple(fields)
UserAdmin.list_display = ("username", "email", "profile_pic", "rsvp",)
UserAdmin.list_filter = ("username", "email",)


admin.site.register(RSVP, RSVPAdmin)
admin.site.register(RegistryEntry, RegistryAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostVersion, PostVersionAdmin)
admin.site.register(CustomUser, UserAdmin)
