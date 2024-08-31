from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract room name from URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()
        
    async def disconnect(self, code):
            await self.channel_layer.group_discard(
             self.room_group_name,
             self.channel_name
    )
    async def receive(self, text_data):
         data=json.loads(text_data)
         message=data['message']
         sender=data['sender']
         await self.channel_layer.group_send(
             
             self.room_group_name,
             {
                 'type':'chat_message',
                 'message':message,
                 'sender':sender
             }
             
         )
        #  event handler for chat message
         def chat_message(self,event):
             message=event['message']
             sender=event['sender']
             self.send(
                text_data= json.dumps({
                    'message':message,
                    'sender':sender,
                })
             )
         

            
        
