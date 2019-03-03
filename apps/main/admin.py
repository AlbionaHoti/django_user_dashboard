from django.contrib import admin
from .models import User
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# Register your models here.

class UserAdmin(admin.ModelAdmin):
  fieldsets = [
    ("Register/info", {"fields": ["first_name", "last_name"]}),
    ("Login/info", {"fields": ["email", "pw_hash", "is_admin"]})
  ]
admin.site.register(User, UserAdmin)
