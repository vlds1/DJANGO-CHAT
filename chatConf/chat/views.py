from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .models import ChatRoomModel, PrivateChat, ChatRoomMessage, PrivateChatMessage


def joinPage(request):
    return render(request, "chat/join_chat.html")

#get page of all chats of a user
@login_required(login_url="login_page")
def chats_list(request):
    context = {
        "user": request.user.id,
        "user_name": request.user.username,
    }
    return render(request, "chat/chats_list.html", context)


#view to join a chat room
@login_required(login_url="login_page")
def getChatRoom(request, chat_name):
    context = {
        "chat_name": chat_name,
        "user": request.user.id,
        "user_name": request.user.username,
        "chat_type": 'public'
    }
    return render(request, "chat/chat.html", context)

#view to join a private chat
@login_required(login_url="login_page")
def getPrivateChat(request, contacts_user):
    current_user_id = User.objects.get(id=request.user.id)
    contact_user_id = User.objects.get(id=contacts_user)
    try:
        try:
            private_chat = PrivateChat.objects.get(
                user1 = current_user_id,
                user2 = contact_user_id
            )
        except ObjectDoesNotExist:
            private_chat = PrivateChat.objects.get(
                user1 = contact_user_id,
                user2 = current_user_id
            )
    except ObjectDoesNotExist:
        private_chat = PrivateChat.objects.create(
            user1 = current_user_id,
            user2 = contact_user_id,
            chat_room_name = f'{current_user_id}_{contact_user_id}'
        )
        private_chat.save()
    
    friend = private_chat.chat_room_name.replace('_', '')
    friend = friend.replace(request.user.username, '')
    context = {
        "chat_name": private_chat.chat_room_name,
        "friend": friend,
        "user": request.user.id,
        "user_name": request.user.username,
        "chat_type": 'private'
    }
    return render(request, "chat/chat.html", context)

#recive all chats of a user
def get_all_chat_rooms(user):
    chat_rooms = ChatRoomModel.objects.values("id", "chat_room_name").filter(
        participant=user.id
    )
    chat_rooms_list = [chat for chat in chat_rooms]
    return chat_rooms_list


#recive all messages of a chat when a user joins it
def get_chat_room_messages(chat_room_id):
    messages_set = ChatRoomMessage.objects.values("text", "sender_id", "id").filter(
        room_chat_id=chat_room_id
    )

    messages = []
    for message in messages_set:
        user = User.objects.get(id=message["sender_id"])
        message["sender_id"] = user.username
        messages.append(message)

    return messages

#recive messages of a private chat with some user
def get_private_chat_messages(chat_room_id):
    messages_set = PrivateChatMessage.objects.values("text", "sender_id", "id").filter(
        room_chat_id=chat_room_id
    )

    messages = []
    for message in messages_set:
        user = User.objects.get(id=message["sender_id"])
        message["sender_id"] = user.username
        messages.append(message)

    return messages
