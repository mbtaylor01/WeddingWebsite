from django.contrib import admin
from .models import RSVP, RegistryEntry, Thread, Post, CustomUser
from django.contrib.auth.admin import UserAdmin

fields = list(UserAdmin.fieldsets)
fields[0] = (None, {'fields': ('username', 'password', 'profile_pic')})
UserAdmin.fieldsets = tuple(fields)


admin.site.register(RSVP)
admin.site.register(RegistryEntry)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(CustomUser, UserAdmin)
