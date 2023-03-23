from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . import api

urlpatterns = [
    path('register', views.user_register, name='user_register'),
    path('login', views.user_login, name='user_login'),
    path('profile', views.user_profile, name='user_profile'),
    path('editProfile', views.user_editProfile, name='user_editProfile'),
    path('search', views.user_search, name='user_search'),
    path('logout', views.user_logout, name='user_logout'),
    path('acceptRequest/<req_id>/', views.acceptRequest, name="acceptRequest"),
    path('declineRequest/<req_id>/', views.declineRequest, name="declineRequest"),
    path('api/user/', api.UserList.as_view(), name='users_api'),
    path('api/user/<int:pk>/', api.UserDetail.as_view(), name='user_detail_api'), 
    path('api/createuser/', api.CreateUser.as_view(), name='createusers_api'),

] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)