from django.urls import path
from .views import *


urlpatterns = [
    path('register/', Auth.register_user, name='register_page'),
    path('login/', Auth.login_user, name='login_page'),
    path('logout/', Auth.logout_user, name='logout'),
]
