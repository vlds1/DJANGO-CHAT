from django.urls import path
from .views import *

urlpatterns = [
    path('', joinPage, name='join_chat'),
    path('chats/', mainPage, name='chats_list'),
    path('chats/<str:chat_name>/', getChat, name='get_chat')
]

