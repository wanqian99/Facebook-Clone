from django.contrib import admin
from .models import *
# Register your models here.

class FriendAdmin(admin.ModelAdmin):
    list_filter = ['id', 'current_user']
    list_display = ['id', 'current_user']
    search_fields = ['id', 'current_user']

    class Meta:
        model = Friend


class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['id', 'sender', 'receiver', 'pending']
    list_display = ['id', 'sender', 'receiver', 'pending']
    search_fields = ['sender__username', 'sender__email', 'receiver_username', 'receiver__email']

    class Meta:
        model = FriendRequest
    
    
admin.site.register(Friend, FriendAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)