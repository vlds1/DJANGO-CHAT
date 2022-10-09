from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .forms import *

# Create your views here.
class Auth:
    
    @staticmethod
    def register_user(request):
        if request.user.is_authenticated == True:
            return redirect('chats_list')
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.set_password(user.password)
                user.save()
                return redirect('login_page')
            
        form = UserRegisterForm()
        context = {
            'form': form
            }
        return render(request, 'register/register_page.html', context)
    
    @staticmethod
    def login_user(request):
        if request.user.is_authenticated == True:
            return redirect('chats_list')
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            print(username, password)
            user = authenticate(
                request, 
                username=username, 
                password=password
            )
            if user is not None:
                login(request, user)
                return redirect('chats_list')
            
        form = UserLoginForm()
        context = {
            'form': form
            }
        return render(request, 'register/login_page.html', context)
            
    
    @staticmethod
    def logout_user(request):
        logout(request)
        return redirect('join_chat')