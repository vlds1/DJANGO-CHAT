from django.contrib import admin
from .models import PrivateChat, PrivateChatMessage, \
                    PublicChat, PublicChatMessage

class PrivateChatAdmin(admin.ModelAdmin):
    list_display = ['chat_room_name', 'addition_time']
    

class PrivateChatMessageAdmin(admin.ModelAdmin):
    list_display = ['room_chat', 'sender', 'text', 'send_time']

admin.site.register(PrivateChat, PrivateChatAdmin)
admin.site.register(PrivateChatMessage, PrivateChatMessageAdmin)


class ChatRoomModelAdmin(admin.ModelAdmin):
    fields = ('owner', 'chat_room_name')
    list_display = ['owner', 'chat_room_name', 'addition_time']
    

class ChatRoomMessageAdmin(admin.ModelAdmin):
    fields = ('text',)
    list_display = ['room_chat', 'sender', 'text', 'send_time']

admin.site.register(PublicChat, ChatRoomModelAdmin)
admin.site.register(PublicChatMessage, ChatRoomMessageAdmin)
