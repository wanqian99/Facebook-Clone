from rest_framework import serializers
from .models import *
from userAccounts.serializers import *


class FriendSerializer(serializers.ModelSerializer):
    current_user = UserSerializer()
    friends = UserSerializer(many=True)
    class Meta:
        model = Friend
        fields = ['pk', 'current_user','friends']


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()
    class Meta:
        model = FriendRequest
        fields = ['pk', 'sender', 'receiver', 'pending', 'timestamp']