from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chat.services.views_service import get_private_chat_service


def joinPage(request):
    """The main page of the app"""
    return render(request, "chat/join_chat.html")

@login_required(login_url="login_page")
def chats_list(request):
    """get page of all public chats of a user"""
    context = {
        "user": request.user.id,
        "user_name": request.user.username,
    }
    return render(request, "chat/chats_list.html", context)

@login_required(login_url="login_page")
def getChatRoom(request, chat_name):
    """Join a public chat room"""
    context = {
        "chat_name": chat_name,
        "user": request.user.id,
        "user_name": request.user.username,
        "chat_type": 'public'
    }
    return render(request, "chat/chat.html", context)

@login_required(login_url="login_page")
def getPrivateChat(request, contacts_user):
    """join a private chat"""
    private_chat = get_private_chat_service(
                    current_user_id = request.user.id,
                    contact_user_id = contacts_user
                    )
    print("PRIVATE_CHAT: ",private_chat)
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
