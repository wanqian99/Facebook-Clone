from django.urls import include, path
from . import views
from . import api

urlpatterns = [
    path('friendDetail/<str:username>', views.friendDetail, name='friendDetail'),
    path('sendRequest/', views.sendRequest, name="sendRequest"),
    path('cancelRequest/', views.cancelRequest, name="cancelRequest"),    
    path('removeFriend/', views.removeFriend, name="removeFriend"),
    path('acceptRequest/<req_id>/', views.acceptRequest, name="acceptRequest"),
    path('declineRequest/<req_id>/', views.declineRequest, name="declineRequest"),
    path('api/friendlist/<int:pk>/', api.FriendDetail.as_view(), name='friends_api'),
    path('api/friendrequest/<int:pk>/', api.FriendRequest.as_view(), name='friend_request_api'),
]