from .models import *
from .forms import *
from .serializers import *

from rest_framework import generics
from rest_framework import mixins

# api/userpost/<int:pk>/
class UserPostList(generics.GenericAPIView, mixins.RetrieveModelMixin):
    # get model table
    queryset = UserPost.objects.all()
    # get serializer class
    serializer_class = UserPostSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# api/createpost/
class CreatePost(generics.GenericAPIView, mixins.CreateModelMixin):
    # get model table
    queryset = UserPost.objects.all()
    # get serializer class
    serializer_class = UserPostSerializer
    # get form class
    form_class = UserPostForm

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)