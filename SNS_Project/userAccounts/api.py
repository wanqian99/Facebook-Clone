from .forms import *
from .models import *
from .serializers import *

from rest_framework import generics
from rest_framework import mixins

# api/user/
class UserList(generics.ListAPIView):
    # get model table
    queryset = UserAccount.objects.all()
    # get serializer class
    serializer_class = UserAccountSerializer


# api/user/<int:pk>/
class CreateUser(generics.GenericAPIView, mixins.CreateModelMixin):
    # get model table
    queryset = User.objects.all()
    # get serializer class
    serializer_class = UserSerializer
    # get form class
    form_class = UserForm

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# api/createuser/
class UserDetail(generics.GenericAPIView, mixins.RetrieveModelMixin):
    # get model table
    queryset = UserAccount.objects.all()
    # get serializer class
    serializer_class = UserAccountSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)