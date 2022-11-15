from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .services import ContactListService

class ContactView:
    @staticmethod
    def get_contacts(request):
        """get contacts list of a user"""
        users_contact = ContactListService.get_user_contact_list(request.user.id) 
        context = {
            "user": request.user.id,
            "user_name": request.user.username,
            'users_contact': users_contact
        }
        return render(request, 'contacts/users_contacts.html', context)

    @staticmethod
    def get_all_users(request):
        """get list of all users"""
        users = User.objects.values('id', 'username').all()
        context = {
            "user": request.user.id,
            "user_name": request.user.username,
            'users': users
        }
        return render(request, 'contacts/all_users.html', context)

    @staticmethod
    def add_contact(request, id):
        """add contact to user's list"""
        ContactListService.add_user_contac_list(
            curent_user_id = request.user.id,
            user_to_add_id = id
            )
        return redirect('contacts')

    @staticmethod
    def delete_contact(request, id):
        """delete a contact from user's contacts list"""
        ContactListService.delete_user_from_contacs_list(
            curent_user_id = request.user.id, 
            user_to_delete_id = id
            )
        return redirect('contacts')