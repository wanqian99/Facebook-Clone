from rest_framework import serializers
from .models import *
from userAccounts.serializers import *

class UserPostSerializer(serializers.ModelSerializer):
    # used to get user data
    user = UserSerializer()
    # define model and fields
    class Meta:
        model = UserPost
        fields = ['pk', 'user', 'content','content_image','timestamp']