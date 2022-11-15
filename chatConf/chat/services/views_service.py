from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from chat.models import PrivateChat


def get_private_chat_service(current_user_id, contact_user_id):
    current_user = User.objects.get(id=current_user_id)
    contact_user = User.objects.get(id=contact_user_id)
        
    try:
        private_chat = PrivateChat.objects.get(
            chat_room_name = f'{contact_user}_{current_user}'
        )
        return private_chat
    except ObjectDoesNotExist:
        private_chat = PrivateChat.objects.get_or_create(
            user1 = current_user,
            user2 = contact_user,
            chat_room_name = f'{current_user}_{contact_user}'
        )
        return private_chat[0]