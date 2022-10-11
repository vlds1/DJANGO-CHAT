from django.db import models
from django.contrib.auth.models import User

class ChatRoomModel(models.Model):
    """Chat room that can join anyone"""
    
    owner = models.ForeignKey(
        User, verbose_name='Owner of chat room', 
        related_name='room_owner',on_delete=models.CASCADE
        )
    participant = models.ManyToManyField(
        User, verbose_name='Participant of chat room',
        related_name='room_participant'
        )
    chat_room_name = models.CharField('Room name', max_length=20, unique=True)
    addition_time = models.DateTimeField('Time of addition', auto_now_add=True)

    def __str__(self):
        return self.chat_room_name

    class Meta:
        db_table = 'chat_rooms'
        ordering = ['addition_time']
        verbose_name = 'chat rooms'
        verbose_name_plural = 'chat room'


class ChatRoomMessage(models.Model):
    """Model of message for a chat room"""

    room_chat = models.ForeignKey(
        ChatRoomModel, verbose_name='Chat room', 
        on_delete=models.CASCADE
        )
    sender = models.ForeignKey(
        User, verbose_name='Sender', on_delete=models.CASCADE
        )
    text = models.TextField('Message')
    send_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'chat_room_messages'
        ordering = ['send_time']
        verbose_name = 'messages'
        verbose_name_plural = 'message'
