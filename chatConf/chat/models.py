from django.db import models
from django.contrib.auth.models import User


class PublicChat(models.Model):
    """Public chat that can join anyone"""
    owner = models.ForeignKey(
        User,
        verbose_name="Owner of chat room",
        related_name="room_owner",
        on_delete=models.CASCADE,
        )
    participant = models.ManyToManyField(
        User, verbose_name="Participant of chat room", 
        related_name="room_participant"
        )
    chat_room_name = models.CharField("Room name", max_length=20, unique=True)
    addition_time = models.DateTimeField("Time of addition", auto_now_add=True)

    def __str__(self):
        return self.chat_room_name

    class Meta:
        db_table = "public_chats"
        ordering = ["addition_time"]
        verbose_name = "Public chat"
        verbose_name_plural = "Public chats"


class PublicChatMessage(models.Model):
    """Model of message for a public chat"""
    room_chat = models.ForeignKey(
        PublicChat, verbose_name="Chat room", on_delete=models.CASCADE
        )
    sender = models.ForeignKey(
        User, verbose_name="Sender", related_name='sender', on_delete=models.CASCADE
        )
    text = models.TextField("Message")
    send_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        db_table = "public_chats_messages"
        ordering = ["send_time"]
        verbose_name = "Public chat message"
        verbose_name_plural = "Public chat messages"


class PrivateChat(models.Model):
    """Private chat room for 2 peoples"""
    chat_room_name = models.CharField('Room name', max_length=120, unique=True)
    user1 = models.ForeignKey(
        User, verbose_name='Chat owner',
        related_name='+', on_delete=models.CASCADE
        )
    user2 = models.ForeignKey(
        User, verbose_name='Chat opponent',
        on_delete=models.CASCADE
        )
    addition_time = models.DateTimeField('Time of addition', auto_now_add=True)

    def __str__(self):
        return self.chat_room_name

    class Meta:
        db_table = 'private_chats'
        ordering = ['addition_time']
        verbose_name = 'private chat'
        verbose_name_plural = 'private chats'


class PrivateChatMessage(models.Model):
    """Model of message for a chat room"""
    room_chat = models.ForeignKey(
        PrivateChat, verbose_name="Private chat", on_delete=models.CASCADE
        )
    sender = models.ForeignKey(
        User, verbose_name="Sender", on_delete=models.CASCADE
        )
    text = models.TextField("Message")
    send_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        db_table = "private_chat_messages"
        ordering = ["send_time"]
        verbose_name = "Private chat message"
        verbose_name_plural = "Private chat messages"