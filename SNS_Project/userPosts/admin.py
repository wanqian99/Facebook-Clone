from django.contrib import admin
from .models import *
# Register your models here.

class UserPostAdmin(admin.ModelAdmin):
    list_display=('id', 'user', 'content', 'content_image', 'timestamp')

admin.site.register(UserPost, UserPostAdmin)