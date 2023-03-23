from rest_framework import serializers
from .models import *
from userAccounts.serializers import *

class ChatroomSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True)
    class Meta:
        model = Chatroom
        fields = ['pk', 'chatroom','user']

class ChatroomContentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True)
    chatroom = ChatroomSerializer()
    class Meta:
        model = ChatroomContent
        fields = ['pk', 'content', 'timestamp', 'user', 'chatroom']