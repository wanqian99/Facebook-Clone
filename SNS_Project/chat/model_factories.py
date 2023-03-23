import factory
from .models import *
from userAccounts.model_factories import *

class ChatroomFactory(factory.django.DjangoModelFactory):
    chatroom = 'testchatroom'
    # user = factory.SubFactory(UserFactory)

    class Meta:
        model = Chatroom

class ChatroomContentFactory(factory.django.DjangoModelFactory):
    content = "chat msg 1"
    timestamp = "July 17, 2022, 2:15 p.m."
    user = factory.SubFactory(UserFactory)
    chatroom = factory.SubFactory(ChatroomFactory)

    class Meta:
        model = ChatroomContent