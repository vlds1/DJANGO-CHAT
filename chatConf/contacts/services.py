from django.contrib.auth.models import User
from .models import ContactsList


class ContactListService:
    """Manage user's contact list"""
    def get_user_contact_list(user_id):
        curent_user = User.objects.get(pk=user_id)
        contacts_list = ContactsList.objects.get_or_create(
            user=curent_user
            )
        users_contact = ContactsList.objects.raw(
            f'SELECT * FROM user_contacts_list_contacts \
                WHERE contactslist_id={contacts_list[0].id};'
            )
        return users_contact

    def add_user_contac_list(user_id):
        currend_user = User.objects.get(pk=user_id)
        contacts_list = ContactsList.objects.get_or_create(
            user = currend_user
        )
        contact = User.objects.get(pk=id)
        contacts_list[0].contacts.add(contact)

    def delete_user_from_contacs_list(user_id):
        contact_list = ContactsList.objects.get(user_id=user_id)
        contact = User.objects.get(id=id)
        contact_list.contacts.remove(contact)