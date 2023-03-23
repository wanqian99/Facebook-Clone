from django.urls import re_path
from . import consumers

# NOTE USE OF ws/ to separate out our ws URIs, like rest use of api/
# python list of websocketurlpatterns
websocket_urlpatterns = [
    # ws for websocket
    # capture any string after ws that's going to be the room name
    # send anything like this that we capture through our chat consumer code
    re_path(r'ws/chat/(?P<chatroom>\w+)/$', consumers.ChatConsumer.as_asgi()),
]