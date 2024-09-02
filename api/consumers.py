import json
from channels.generic.websocket import AsyncWebsocketConsumer
from . models import Message,MyUser,Chatroom
from . import models
from asgiref.sync import sync_to_async
from django.core.exceptions import ValidationError

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        

        # Join room group
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id=text_data_json['sender_id']
        # Fetching the Sender data
        sender=await sync_to_async(MyUser.objects.get)(id=sender_id)
        # fetching the chatroom 
        chat_room=await sync_to_async(Chatroom.objects.get(id=self.room_name))
        await self.save_messages(chat_room,sender,message)
        
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type':'chat_message',
                'message':message,
                'sender_name':sender.name
            }
        )
        
    async def chat_message(self, event):
        message = event['message']
        sender_name = event['sender_name']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_name': sender_name,
        }))
            

            
            
        
async def save_messages(self, chat_room, sender, message):
    if sender != chat_room.user1 and sender != chat_room.user2:
        raise ValidationError("Sender must be one of the users in the chatroom")
    
    try:
        await sync_to_async(Message.objects.create)(
            chat_room=chat_room,
            sender=sender,
            content=message
        )
    except ValidationError as e:
        # Handle the error appropriately
        print(f"Validation Error: {e}")

        
        
        
        
        
        
        






