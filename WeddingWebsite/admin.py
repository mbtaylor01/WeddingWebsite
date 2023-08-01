from django.contrib import admin
from .models import RSVP, RegistryEntry, Thread, Post, CustomUser
from django.contrib.auth.admin import UserAdmin


class PostAdmin(admin.ModelAdmin): 
    list_filter = ("creator", "creation_time", "thread")
    list_display = ("creator", "creation_time", "text", "thread")

class RegistryAdmin(admin.ModelAdmin): 
    list_filter = ("title", "reserved_by")
    list_display = ("title", "reserved_by")

class RSVPAdmin(admin.ModelAdmin): 
    list_filter = ("additional_people", "allergies", "alcohol", "other")
    list_display = ("user", "additional_people", "allergies", "alcohol", "other")

    def user(self, instance):
        # display one-to-one linked customuser.username field in Admin panel
        try:
            return instance.customuser.username
        except RSVP.customuser.RelatedObjectDoesNotExist:
            pass

class ThreadAdmin(admin.ModelAdmin): 
    list_filter = ("creator", "creation_time",)
    list_display = ("title", "creator", "creation_time",)


fields = list(UserAdmin.fieldsets)
fields[0] = (None, {'fields': ('username', 'password', 'profile_pic', 'rsvp')})
UserAdmin.fieldsets = tuple(fields)
UserAdmin.list_display = ("username", "email", "profile_pic", "rsvp",)
UserAdmin.list_filter = ("username", "email",)


admin.site.register(RSVP, RSVPAdmin)
admin.site.register(RegistryEntry, RegistryAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(CustomUser, UserAdmin)
