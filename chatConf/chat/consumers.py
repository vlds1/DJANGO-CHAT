# chat/consumers.py
import json
from random import randint
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

        
class ChatsListConsumer(WebsocketConsumer):
    """connecting to list of chats page"""
    def connect(self):
        self.accept()
        
    def disconnect(self, code):
        pass
        
    def receive(self, text_data):
        chat_name = json.loads(text_data)
        
        self.send(json.dumps(chat_name))
        
        
        
class ChatRoom(WebsocketConsumer):
    def connect(self):
        self.chat_name = self.scope['url_route']['kwargs']['room_name'] 
        self.chat_group_name = 'chat_%s' % self.chat_name
        self.user_id = randint(1, 999)
        
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
        
        message = str(self.user_id) + ': ' + data['message']
        
        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        
    def chat_message(self, event):
        message = event['message']
        
        self.send(text_data=json.dumps({
            'message': message
        }))