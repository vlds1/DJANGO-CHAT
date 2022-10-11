from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatRoomModel, ChatRoomMessage

# Create your views here.
def joinPage(request):
    return render(request, 'chat/join_chat.html')

@login_required(login_url='login_page')
def mainPage(request):
    context = {
        'user': request.user.id
    }
    return render(request, 'chat/chats_list.html', context)

@login_required(login_url='login_page')
def getChat(request, chat_name):
    context = {
        'chat_name': chat_name,
        'user': request.user.id
    }
    return render(request, 'chat/chat.html', context)

def get_all_chat_rooms(user):
    chat_rooms = ChatRoomModel.objects.values(
        'id', 'chat_room_name'
        ).filter(participant=user.id)
    chat_rooms_list = [chat for chat in chat_rooms]
    return chat_rooms_list

def get_chat_room_messages(chat_room_id):
    messages_set = ChatRoomMessage.objects.values(
        'text', 'sender_id'
        ).filter(room_chat_id=chat_room_id)
    messages = [message for message in messages_set]
    return messages