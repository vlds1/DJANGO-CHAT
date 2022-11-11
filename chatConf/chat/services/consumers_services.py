"""Services to manage user's chat list and its messages"""
from django.contrib.auth.models import User
from chat.models import ChatRoomModel, ChatRoomMessage, PrivateChat, PrivateChatMessage

class ChatRoomService:
    """Class to manage user's chat list"""
    @staticmethod
    def create_chat_room(data):
        """Add chat room to user's chat list \
        and create the chat if this doesnt exists add the user to participant"""
        user = User.objects.get(id=data["user"])
        chat = ChatRoomModel.objects.get_or_create(
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
        """Leave chat room and delete it if its owner of a chat"""
        chat = ChatRoomModel.objects.get(id=data["chat_to_delete"])
        participant = User.objects.get(id=data["user"])
        chat.participant.remove(participant)
        room_id = chat.id
        # delete chat if its owner
        if chat.owner_id == data["user"]:
            chat.delete()
        return room_id

    @staticmethod
    def get_all_chat_rooms(user):
        """Get list of all chat rooms"""
        chat_rooms = ChatRoomModel.objects.values("id", "chat_room_name").filter(
            participant=user.id
        )
        print(chat_rooms)
        chat_rooms_list = [chat for chat in chat_rooms]
        return chat_rooms_list


class ChatMessageService: 
    """Class to manage messages of a chat"""
    @staticmethod
    def create_chat_room_message(data, chat_type, chat_name):
        """Check type of a chat and create a message to send it in the future"""
        if chat_type == 'public':
            new_message = ChatRoomMessage.objects.create(
                room_chat=ChatRoomModel.objects.get(chat_room_name=chat_name),
                sender=User.objects.get(id=data["user"]),
                text=data["message"],
            )
        else:
            new_message = PrivateChatMessage.objects.create(
                room_chat=PrivateChat.objects.get(chat_room_name=chat_name),
                sender=User.objects.get(id=data["user"]),
                text=data["message"],
            )
        new_message.save()

        return new_message

    @staticmethod
    def delete_chat_room_message(data):
        """"Checking chat type and delete a message"""
        if data['chat_type'] == 'private':
            message_to_delete = PrivateChatMessage.objects.get(id=data['message_id'])
            message_to_delete.delete()
        else:
            message_to_delete = ChatRoomMessage.objects.get(id=data['message_id'])
            message_to_delete.delete()

    @staticmethod
    def get_chat_room_messages(chat_room_id):
        """recive all messages of a chat when a user joins it"""
        messages_set = ChatRoomMessage.objects.values(
            "text", "sender_id", "id").filter(
            room_chat_id=chat_room_id
        )

        messages = []
        for message in messages_set:
            user = User.objects.get(id=message["sender_id"])
            message["sender_id"] = user.username
            messages.append(message)

        return messages

    @staticmethod
    def get_private_chat_messages(chat_room_id):
        """recive messages of a private chat with some user"""
        messages_set = PrivateChatMessage.objects.values("text", "sender_id", "id").filter(
            room_chat_id=chat_room_id
        )

        messages = []
        for message in messages_set:
            user = User.objects.get(id=message["sender_id"])
            message["sender_id"] = user.username
            messages.append(message)

        return messages
