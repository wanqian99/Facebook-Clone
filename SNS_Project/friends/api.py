from .models import *
from .serializers import *

from rest_framework import generics
from rest_framework import mixins

# api/friendlist/<int:pk>/
class FriendDetail(generics.ListAPIView, mixins.RetrieveModelMixin):
    # get model table
    queryset = Friend.objects.all()
    # get serializer class
    serializer_class = FriendSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# api/friendrequest/<int:pk>/
class FriendRequest(generics.ListAPIView, mixins.RetrieveModelMixin):
    # get model table
    queryset = FriendRequest.objects.all()
    # get serializer class
    serializer_class = FriendRequestSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)