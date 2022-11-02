from django.urls import path
from .views import joinPage, chats_list, getChatRoom, getPrivateChat

urlpatterns = [
    path("", joinPage, name="join_chat"),
    path("chats/", chats_list, name="chats_list"),
    path("chats/<str:chat_name>/", getChatRoom, name="get_chat"),
    path("chats/private/<str:contacts_user>/", getPrivateChat, name="get_private_chat"),
]
