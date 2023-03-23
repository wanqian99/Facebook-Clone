from .models import *
from .serializers import *

from rest_framework import generics
from rest_framework import mixins

class ChatroomList(generics.GenericAPIView, mixins.RetrieveModelMixin):
    # get model table
    queryset = Chatroom.objects.all()
    # get serializer class
    serializer_class = ChatroomSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)