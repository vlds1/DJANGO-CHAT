from django.urls import path, re_path
from .consumers import ChatsListConsumer, ChatRoom

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    path("ws/chat/list/", ChatsListConsumer.as_asgi()),
    path("ws/chat/<str:chat_type>/<str:room_name>/", ChatRoom.as_asgi()),
]
