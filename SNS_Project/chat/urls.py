from django.urls import include, path
from . import views
from . import api

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('chat/<str:chatroom_name>', views.room, name='room'),
    path('chat/deleteChatroom/<str:chatroom_name>', views.deleteChatroom, name='deleteChatroom'),
    path('api/chatroom/<int:pk>/', api.ChatroomList.as_view(), name='chatroom-api'),
]