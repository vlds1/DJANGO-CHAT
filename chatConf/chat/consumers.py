# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from .models import ChatRoomModel, ChatRoomMessage
from .views import get_all_chat_rooms, get_chat_room_messages


class ChatsListConsumer(WebsocketConsumer):
    """connecting to list of chats page"""

    def create_chat_room(self, data):
        # if chat exists its just add participant to it    
        try:
            chat_exists = ChatRoomModel.objects.get(chat_room_name=data['chat_name'])
            user = User.objects.get(id=data['user'])
            chat_exists.participant.add(user)
            chat = {
                'id': str(chat_exists.id),
                'chat_room_name': chat_exists.chat_room_name
            }
            self.send(json.dumps({'chats':chat, 'command':'create_new_chat'}))

        # if chat doesnt exists its create it and add owner to participants
        except:
            creator = User.objects.get(id=data['user'])
            new_chat = ChatRoomModel.objects.create(
                owner = creator,
                chat_room_name = data['chat_name']
                )
            new_chat.save()
            new_chat.participant.add(creator)
            chat = {
                'id': str(new_chat.id),
                'chat_room_name': new_chat.chat_room_name
                }
            self.send(json.dumps({'chats':chat, 'command':'create_new_chat'}))

    def delete_chat_room(self, data):
            chat = ChatRoomModel.objects.get(id=data['chat_to_delete'])
            participant = User.objects.get(id=data['user'])
            chat.participant.remove(participant)
            room_id = chat.id
            #delete chat if its owner
            if chat.owner_id == data['user']:
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
        self.user = self.scope['user']
        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name,
            self.channel_name   
        )

        chat_room = ChatRoomModel.objects.get(chat_room_name=self.chat_name)
        messages = get_chat_room_messages(chat_room.id)
        for message in messages:
            async_to_sync(self.channel_layer.group_send)(
                self.chat_group_name,
                {
                    'type': 'chat_message',
                    'message': message['text'],
                    'user': message['sender_id']
                }
            )
        self.accept()
        
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_name,
            self.channel_name
        )
    
    def receive(self, text_data):
        data = json.loads(text_data)
        
        new_message = ChatRoomMessage.objects.create(
            room_chat = ChatRoomModel.objects.get(chat_room_name=self.chat_name),
            sender = User.objects.get(id=data['user']),
            text = data['message']
        )
        new_message.save()
        
        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': new_message.text,
                'user': int(new_message.sender_id)
            }
        )
        
    def chat_message(self, event):
        message = event['message']
        user = User.objects.get(id=event['user'])
        self.send(text_data=json.dumps({
            'message': message,
            'user': user.username
        }))