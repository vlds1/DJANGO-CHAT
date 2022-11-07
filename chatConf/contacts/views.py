from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import ContactsList


class ContactView:
    #get contacts list of a user
    @staticmethod
    def get_contacts(request):
        curent_user = User.objects.get(pk=request.user.id)
        contacts_list = ContactsList.objects.get_or_create(
            user=curent_user
            )
        users_contact = ContactsList.objects.raw(
            f'SELECT * FROM user_contacts_list_contacts \
                WHERE contactslist_id={contacts_list[0].id};'
            )
        context = {
            "user": request.user.id,
            "user_name": request.user.username,
            'users_contact': users_contact
        }
        return render(request, 'contacts/users_contacts.html', context)

    #get all users
    @staticmethod
    def get_all_users(request):
        users = User.objects.values('id', 'username').all().order_by('-username')

        context = {
            "user": request.user.id,
            "user_name": request.user.username,
            'users': users
        }
        return render(request, 'contacts/all_users.html', context)

    #add contact to user's list
    @staticmethod
    def add_contact(request, id):
        currend_user = User.objects.get(pk=request.user.id)
        contacts_list = ContactsList.objects.get_or_create(
            user = currend_user
        )
        contact = User.objects.get(pk=id)
        contacts_list[0].contacts.add(contact)

        return redirect('contacts')

    @staticmethod
    def delete_contact(request, id):
        contact_list = ContactsList.objects.get(user_id=request.user.id)
        contact = User.objects.get(id=id)
        contact_list.contacts.remove(contact)
        return redirect('contacts')