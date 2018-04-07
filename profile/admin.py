from django.contrib import admin

from .models import Profile,UserFile

admin.site.register(UserFile)
admin.site.register(Profile)
