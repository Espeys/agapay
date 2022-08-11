"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""
import os

from asgiref.sync import async_to_sync
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.generic.websocket import WebsocketConsumer

from django.core.asgi import get_asgi_application
from django.urls import path, re_path, include

from time import sleep


import json
import random

from apps.account.models import ChatRoom, Message, Profile
from apps.account.serializers import MessageSerializer

from rest_framework.renderers import JSONRenderer


class ChatMessageConsumer(WebsocketConsumer):

    def connect(self):
        self.room_slug = self.scope['url_route']['kwargs']['slug']
        self.room_group_name = 'chat_%s' % self.room_slug

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        slug = text_data_json.get('slug', None) # status
        message = text_data_json.get('message', None)# message
        sender = text_data_json.get('sender', None)

        if slug:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    'type': 'chat_remove',
                    'slug': slug
                }
            )

        elif message: # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender,
                }
            )

    def chat_remove(self, event):
        slug = event['slug']

        profile = Profile.people.state_active().get(slug=self.user_slug)
        chatroom = ChatRoom.objects.get(slug=self.room_slug, members__in=[profile])
        m = Message.objects.get(slug=slug, chatroom=chatroom, created_by=profile)
        m.state = Message.STATE_INACTIVE
        m.is_readed = True
        m.save()

        m_serialize = MessageSerializer(m).data

        self.send(text_data=json.dumps({
            'slug': m_serialize['slug'],
            'chatroom_slug': m_serialize['chatroom_slug'],
            'text': m_serialize['text'],
            'is_readed': m_serialize['is_readed'],
            'created_at': m_serialize['created_at'],
            'created_by': m_serialize['created_by']
        }))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        profile = Profile.people.state_active().get(slug=sender)
        chatroom = ChatRoom.objects.get(slug=self.room_slug, members__in=[profile]) # wew
        m = Message.objects.create(text=message, chatroom=chatroom, created_by=profile)
        m.seen_by.add(profile)
        m.is_readed = True
        m_serialize = MessageSerializer(m).data

        self.send(text_data=json.dumps({
            'slug': m_serialize['slug'],
            'chatroom_slug': m_serialize['chatroom_slug'],
            'text': m_serialize['text'],
            'is_readed': m_serialize['is_readed'],
            'created_at': m_serialize['created_at'],
            'created_by': m_serialize['created_by']
        }))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/chat/message/(?P<slug>[-@\w]+)/$', ChatMessageConsumer.as_asgi())
        ])
    )
})
