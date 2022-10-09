# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from .models import ChatRoomModel
from .views import get_all_chat_rooms


class ChatsListConsumer(WebsocketConsumer):
    """connecting to list of chats page"""

    def create_chat_room(self, data):
        new_chat = ChatRoomModel.objects.create(
            participant = User.objects.get(id=data['user']),
            chat_room_name = data['chat_name']
        )
        chat = {
            'id': str(new_chat.id),
            'chat_room_name': new_chat.chat_room_name
        }
        self.send(json.dumps({'chats':chat, 'command':'create_new_chat'}))

    def delete_chat_room(self, data):
        chat = ChatRoomModel.objects.get(id=data['chat_to_delete'])
        room_id = chat.id
        chat.delete()
        self.send(json.dumps({'id': room_id, 'command':'deleted'}))

    commands = {
        'create_chat_room': create_chat_room,
        'delete_chat_room': delete_chat_room
    }

    def connect(self):
        self.accept()
        chats = get_all_chat_rooms(self.scope['user'])
        self.send(json.dumps({'chats':chats, 'command': 'get_all_chats'}))
        
    def disconnect(self, code):
        pass
        
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)
        
        
class ChatRoom(WebsocketConsumer):
    """Consumer for a general chat room"""

    def connect(self):
        self.chat_name = self.scope['url_route']['kwargs']['room_name'] 
        self.chat_group_name = 'chat_%s' % self.chat_name
        self.user = self.scope['user'].username

        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name,
            self.channel_name   
        )
        
        self.accept()
        
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_name,
            self.channel_name
        )
    
    def receive(self, text_data):
        data = json.loads(text_data)
        
        message = data['message']
        
        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user
            }
        )
        
    def chat_message(self, event):
        message = event['message']
        user = event['user']
        self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))