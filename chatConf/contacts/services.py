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
            
        # contacts = (
        #     ContactsList.objects
        #     .prefetch_related('contacts')
        #     .filter(contacts=contacts_list[0].id)
        # )
        # for contact in contacts:
        #     print(contact.contacts.all())

        return users_contact

    def add_user_contac_list(curent_user_id, user_to_add_id):
        currend_user = User.objects.get(pk=curent_user_id)
        contacts_list = ContactsList.objects.get_or_create(
            user = currend_user
        )
        contact = User.objects.get(pk=user_to_add_id)
        contacts_list[0].contacts.add(contact)

    def delete_user_from_contacs_list(curent_user_id, user_to_delete_id):
        contact_list = ContactsList.objects.get(user_id=curent_user_id)
        contact = User.objects.get(id=user_to_delete_id)
        contact_list.contacts.remove(contact)