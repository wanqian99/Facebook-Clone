from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    # define model and fields
    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name', 'email', 'password']


class UserAccountSerializer(serializers.ModelSerializer):
    # used to get user data
    user = UserSerializer()
    # define model and fields
    class Meta:
        model = UserAccount
        fields = ['pk', 'user', 'image','phone_number','dob']