import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Safely query message from a CharField
        latest_message = await sync_to_async(
            lambda: Message.objects.filter(room_name=self.room_name).latest('timestamp')
        )()
        sender_username = await sync_to_async(lambda: latest_message.sender.username)()

        await self.send(text_data=json.dumps({
            'sender': sender_username,
            'message': latest_message.content
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_username = data['sender']
        receiver_username = data.get('receiver')  # make sure frontend sends this

        sender = await sync_to_async(User.objects.get)(username=sender_username)
        receiver = await sync_to_async(User.objects.get)(username=receiver_username)

        new_message = await sync_to_async(Message.objects.create)(
            sender=sender,
            receiver=receiver,
            content=message,
            room_name=self.room_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

