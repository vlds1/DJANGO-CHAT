import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from chat.services.consumers_services import ChatMessageService, ChatRoomService

class ChatsListConsumer(WebsocketConsumer):
    """connecting to list of chats page""" 
    def create_chat_room(self, data):
        """Checking if chat exists and add user to participant
        or creating this and add to participant"""
        data = ChatRoomService.create_chat_room(data)
        self.send(json.dumps({"chats": data, "command": "create_new_chat"}))

    def delete_chat_room(self, data):
        """Delete public chat room by its id"""
        room_id = ChatRoomService.delete_chat_room(data)
        self.send(json.dumps({"id": room_id, "command": "deleted"}))

    commands = {
        "create_chat_room": create_chat_room,
        "delete_chat_room": delete_chat_room,
    }

    def connect(self):
        self.accept()
        chats = ChatRoomService.get_all_chat_rooms(self.scope["user"])
        self.send(json.dumps({"chats": chats, "command": "get_all_chats"}))

    def disconnect(self, code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)


class ChatRoom(WebsocketConsumer):
    """Consumer for a general chat room"""
    def create_and_send_message(self, data):
        """Create message to send to a chat"""
        new_message = ChatMessageService.create_chat_message(
            data, self.chat_type, self.chat_name)
        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {
                "type": "send_chat_message",
                "user": int(new_message.sender_id),
                "message": new_message.text,
                "message_id": new_message.id,
            }
        )

    def send_chat_message(self, event):
        """Send created message to users"""
        message = event["message"]
        user = User.objects.get(id=event["user"])
        self.send(text_data=json.dumps({   
                    "command": "create_message",
                    "user": user.username,
                    "message": message,
                    "message_id": str(event["message_id"]),
                }))

    def delete_message(self, data):
        """Identify message and delete it"""
        ChatMessageService.delete_chat_message(data)
        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {   
                'type': 'send_info_about_deleted_message',
                'deleted_message_id': data['message_id']
            }
        )

    def send_info_about_deleted_message(self, event):
        """Send info about deleted message to users"""
        deleted_messaeg_id = event['deleted_message_id']
        self.send(text_data = json.dumps(
            {
                'command': 'delete_message',
                'deleted_messaeg_id': str(deleted_messaeg_id)
            }
        ))


    commands = {
        'delete_message': delete_message,
        'create_message': create_and_send_message,
    }

    def connect(self):
        self.chat_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.chat_group_name = "chat_%s" % self.chat_name
        self.user = self.scope["user"]
        self.chat_type = self.scope["url_route"]["kwargs"]["chat_type"]
        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name, self.channel_name
        )

        self.accept()
        messages = ChatMessageService.get_last_chat_messages(
            chat_type= self.chat_type,
            chat_name = self.chat_name
        )
        self.send(json.dumps({
                "messages": messages, 
                "command": "get_last_messages"
            })
        )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_name, self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)


