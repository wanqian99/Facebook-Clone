from django.contrib import admin
from .models import *
# Register your models here.

class ChatroomAdmin(admin.ModelAdmin):
    list_display = ['pk', 'chatroom']

class ChatroomContentAdmin(admin.ModelAdmin):
    list_display = ['content', 'timestamp', 'user', 'chatroom']

admin.site.register(Chatroom, ChatroomAdmin)
admin.site.register(ChatroomContent, ChatroomContentAdmin)