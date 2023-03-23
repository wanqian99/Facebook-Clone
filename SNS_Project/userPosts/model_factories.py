import factory
from .models import *
from userAccounts.model_factories import *

class UserPostFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    content = "Hello!!"
    content_image = "./static/userAccounts/user.png"
    timestamp = "July 17, 2022, 2:15 p.m."

    class Meta:
        model = UserPost