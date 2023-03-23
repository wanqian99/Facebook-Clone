import factory
from .models import *

class UserFactory(factory.django.DjangoModelFactory):
    username = 'testuser'
    email = 'testuser@gmail.com'
    first_name = 'apple'
    last_name = 'pineapple'
    password = 'testuserpassword'

    class Meta:
        model = User

class UserAccountFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    image = "./static/userAccounts/user.png"
    phone_number = "80008008"
    dob = "2000-10-10"

    class Meta:
        model = UserAccount