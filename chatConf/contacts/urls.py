from django.urls import path
from .views import ContactView 

urlpatterns = [
    path('contacts/', ContactView.get_contacts, name='contacts'),
    path('all_users/', ContactView.get_all_users, name='all_users'),
    path('add_contact/<str:id>', ContactView.add_contact, name='add_contact'),
    path('delete_contact/<str:id>', ContactView.delete_contact, name='delete_contact'),
]