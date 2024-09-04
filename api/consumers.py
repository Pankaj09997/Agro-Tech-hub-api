from channels.generic.websocket import AsyncWebsocketConsumer
import json
from api.models import MyUser, ChatModel
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope['user'].id
        other_user_id = self.scope['urlroute']['kwargs']['id']

        if int(user_id) > int(other_user_id):
            self.room_name = f'{user_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{user_id}'

        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        name = text_data_json['name']
        receiver = text_data_json['receiver']

        await self.save_message(name, message, receiver, self.room_name)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'name': name,
                'receiver': receiver
            }
        )

    async def chat_message(self, event):
        message = event['message']
        name = event['name']
        receiver = event['receiver']

        await self.send(text_data=json.dumps({
            'message': message,
            'receiver': receiver,
            'name': name
        }))

    @database_sync_to_async
    def save_message(self, name, message, receiver, room_name):
        user = MyUser.objects.get(id=self.scope['user'].id)
        receiver_user = MyUser.objects.get(id=receiver)
        ChatModel.objects.create(
            name=user,
            receiver=receiver_user,
            room_name=room_name,
            messages=message
        )
