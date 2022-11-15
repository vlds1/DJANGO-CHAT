"""Services to manage user's chat list and its messages"""
from django.contrib.auth.models import User
from chat.models import PublicChat, PublicChatMessage, PrivateChat, PrivateChatMessage

class ChatRoomService:
    """Class to manage user's chat list"""
    @staticmethod
    def create_chat_room(data):
        """Add chat room to user's chat list \
        and create the chat if this doesnt exists add the user to participant"""
        user = User.objects.get(id=data["user"])
        chat = PublicChat.objects.get_or_create(
            owner = user, chat_room_name = data["chat_name"]
            )
        chat[0].participant.add(user)
        chat_data = {
            'id': str(chat[0].id),
            'chat_room_name': chat[0].chat_room_name
            }
        return chat_data

    @staticmethod
    def delete_chat_room(data):
        """Leave chat public chat and delete it if its owner of a chat"""
        chat = PublicChat.objects.get(id=data["chat_to_delete"])
        participant = User.objects.get(id=data["user"])
        chat.participant.remove(participant)
        room_id = chat.id
        if chat.owner_id == data["user"]:   # delete chat if its owner
            chat.delete()
        return room_id

    @staticmethod
    def get_all_chat_rooms(user):
        """Get list of all public chats of a user"""
        chat_rooms = (
            PublicChat.objects
            .values("id", "chat_room_name")
            .filter(participant=user.id)
        )
        return list(chat_rooms)


class ChatMessageService: 
    """Class to manage messages of a chat"""
    @staticmethod
    def create_chat_message(data, chat_type, chat_name):
        """Check type of a chat and create a message to send it in the future"""
        message_model = PublicChatMessage if chat_type == 'public' else PrivateChatMessage
        chat_model = PublicChat if chat_type == 'public' else PrivateChat
        
        new_message = message_model.objects.create(
                room_chat=chat_model.objects.get(chat_room_name=chat_name),
                sender=User.objects.get(id=data["user"]),
                text=data["message"],
            )
        new_message.save()

        return new_message

    @staticmethod
    def delete_chat_message(data):
        """"Checking chat type and delete a message"""
        model = PrivateChatMessage if data['chat_type'] == 'private' else PublicChatMessage
        message_to_delete = model.objects.get(id=data['message_id'])
        message_to_delete.delete()

    @staticmethod
    def get_last_chat_messages(chat_type, chat_name):
        chat_model = PublicChat if chat_type == 'public' else PrivateChat
        message_model = PublicChatMessage if chat_type == 'public' else PrivateChatMessage
        chat = chat_model.objects.get(chat_room_name=chat_name)
        
        messages_queryset = (
            message_model.objects
            .select_related('sender')
            .filter(room_chat_id=chat.id)
            .values('text', 'sender__username', 'id')
        )
        return list(messages_queryset)
