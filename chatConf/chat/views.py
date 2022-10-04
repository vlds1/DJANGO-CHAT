from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
def joinPage(request):
    return render(request, 'chat/join_chat.html')

@login_required(login_url='login_page')
def mainPage(request, ):
    context = {
        'user': request.user.is_authenticated
    }
    return render(request, 'chat/chats_list.html', context)

@login_required(login_url='login_page')
def getChat(request, chat_name):
    context = {
        'chat_name': chat_name
    }
    return render(request, 'chat/chat.html', context)