from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Profile


class ProfileInline(admin.StackedInline):
   model = Profile
   fields = ["avatar", "is_corporate"]


class ProfileAdmin(UserAdmin):
   inlines = [ProfileInline]


User = get_user_model()
admin.site.unregister(User)

admin.site.register(User, ProfileAdmin)
