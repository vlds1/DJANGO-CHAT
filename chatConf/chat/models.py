from django.db import models
from django.contrib.auth.models import User

class ChatRoomModel(models.Model):
    """Chat room that can join anyone"""

    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room_name = models.CharField('Room name', max_length=20)
    addition_time = models.DateTimeField('Time of addition', auto_now_add=True)

    def __str__(self):
        return self.chat_room_name

    class Meta:
        db_table = 'chat_rooms'
        ordering = ['addition_time']
        verbose_name = 'chat rooms'
        verbose_name_plural = 'chat room'


# class PrivateChat(models.Model):
#     """Privat chat room for 2 peoples"""
#     chat_room_name = models.CharField('Room name', max_length=20)
#     owner = models.ForeignKey(
#         User, verbose_name='Chat owner', 
#         related_name='+', on_delete=models.CASCADE
#         )
#     opponent = models.ForeignKey(
#         User, verbose_name='Chat opponent', 
#         on_delete=models.CASCADE
#         )
#     addition_time = models.DateTimeField('Time of addition', auto_now_add=True)

#     def __str__(self):
#         return self.chat_name

#     class Meta:
#         db_table = 'privat_chats'   
#         ordering = ['addition_time']
#         verbose_name = 'privat chats'
#         verbose_name_plural = 'privat chat'


class ChatRoomMessage(models.Model):
    """Model of message for a chat room"""

    room_chat = models.ForeignKey(
        ChatRoomModel, verbose_name='Chat room', on_delete=models.CASCADE)
    sener = models.ForeignKey(
        User, verbose_name='Sender', on_delete=models.CASCADE)
    text = models.TextField('Message')
    send_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'chat_room_messages'
        ordering = ['send_time']
        verbose_name = 'messages'
        verbose_name_plural = 'message'


# class PrivatChatMessage(models.Model):
#     room_chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE)
#     text = models.TextField('Message')
#     send_time = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.text

#     class Meta:
#         db_table = 'chat_room_messages'
#         ordering = ['send_time']
#         verbose_name = 'messages'
#         verbose_name_plural = 'message'
