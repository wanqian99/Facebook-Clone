from django.urls import include, path
from . import views
from . import api

urlpatterns = [
    path('', views.home, name='home'),
    path('api/userpost/<int:pk>/', api.UserPostList.as_view(), name='user_post_api'),
    path('api/createpost/', api.CreatePost.as_view(), name='create_post_api'),
]