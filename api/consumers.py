# from django.utils import timezone  # Correct import
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from api.models import MyUser, Mychats

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope['user']  # User authenticated via JWT token

#         if self.user and self.user.is_authenticated:
#             # Create a room name using the user’s ID to ensure uniqueness
#             self.room_group_name = f'chat_{self.user.id}'

#             # Add user to their own channel group
#             await self.channel_layer.group_add(
#                 self.room_group_name,
#                 self.channel_name
#             )
#             await self.accept()
#         else:
#             await self.close(code=4001)

#     async def disconnect(self, close_code):
#         if self.user.is_authenticated:
#             # Remove the user from their group on disconnect
#             await self.channel_layer.group_discard(
#                 self.room_group_name,
#                 self.channel_name
#             )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         me_id = data['me_id']
#         frnd_id = data['frnd_id']
#         message = data['message']

#         # Save chat message to the database
#         await self.save_chat(me_id, frnd_id, message)

#         # Send the message to the friend (private messaging)
#         frnd_room_group = f'chat_{frnd_id}'
#         await self.channel_layer.group_send(
#             frnd_room_group,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender': me_id,
#             }
#         )

#     async def chat_message(self, event):
#         # Called when a message is sent to the WebSocket
#         message = event['message']
#         sender = event['sender']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'sender': sender,
#         }))

#     @database_sync_to_async
#     def save_chat(self, me_id, frnd_id, message):
#         try:
#             me = MyUser.objects.get(id=me_id)
#             frnd = MyUser.objects.get(id=frnd_id)
#             mychats, _ = Mychats.objects.get_or_create(me=me, frnd=frnd)

#             # Append the new message to the existing chat
#             mychats.chats.append({'sender_id': me_id, 'message': message, 'timestamp': timezone.now().isoformat()})
#             mychats.save()
#         except MyUser.DoesNotExist:
#             pass
# from django.utils import timezone
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from api.models import MyUser, Mychats

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope['user']  # User authenticated via JWT token

#         if self.user and self.user.is_authenticated:
#             # Create a room name using the user’s ID to ensure uniqueness
#             self.room_group_name = f'chat_{self.user.id}'

#             # Add user to their own channel group
#             await self.channel_layer.group_add(
#                 self.room_group_name,
#                 self.channel_name
#             )
#             await self.accept()
#         else:
#             await self.close(code=4001)

#     async def disconnect(self, close_code):
#         if self.user.is_authenticated:
#             # Remove the user from their group on disconnect
#             await self.channel_layer.group_discard(
#                 self.room_group_name,
#                 self.channel_name
#             )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         me_id = int(data['me_id'])  # Ensure IDs are integers
#         frnd_id = int(data['frnd_id'])
#         message = data['message']

#         # Save chat message to the database
#         await self.save_chat(me_id, frnd_id, message)

#         # Send the message to the friend (private messaging)
#         frnd_room_group = f'chat_{frnd_id}'
#         await self.channel_layer.group_send(
#             frnd_room_group,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender': me_id,
#             }
#         )

#     async def chat_message(self, event):
#         # Called when a message is sent to the WebSocket
#         message = event['message']
#         sender = event['sender']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'sender': sender,
#         }))

#     @database_sync_to_async
#     def save_chat(self, me_id, frnd_id, message):
#         try:
#             me = MyUser.objects.get(id=me_id)
#             frnd = MyUser.objects.get(id=frnd_id)
#             mychats, _ = Mychats.objects.get_or_create(me=me, frnd=frnd)

#             # Append the new message to the existing chat
#             mychats.chats.append({'sender_id': me_id, 'message': message, 'timestamp': timezone.now().isoformat()})
#             mychats.save()
#         except MyUser.DoesNotExist:
#             pass

# from django.utils import timezone
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from api.models import MyUser, Mychats

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope['user']  # User authenticated via JWT token

#         if self.user and self.user.is_authenticated:
#             self.user_id = self.user.id

#             # Create a unique room for the user to handle connections
#             self.room_group_name = f'chat_{self.user_id}'

#             # Add the user to their chat group (unique to the user)
#             await self.channel_layer.group_add(
#                 self.room_group_name,
#                 self.channel_name
#             )
#             await self.accept()
#         else:
#             await self.close(code=4001)

#     async def disconnect(self, close_code):
#         if self.user.is_authenticated:
#             # Remove the user from their group on disconnect
#             await self.channel_layer.group_discard(
#                 self.room_group_name,
#                 self.channel_name
#             )

#     async def receive(self, text_data):
#         # Receive and handle the message data
#         data = json.loads(text_data)
#         me_id = self.user.id  # Use the authenticated user's ID as me_id
#         frnd_id = int(data['frnd_id'])  # frnd_id should be sent in the message payload
#         message = data['message']

#         # Save chat message to the database
#         await self.save_chat(me_id, frnd_id, message)

#         # Create a consistent room for private messaging by sorting the user IDs
#         room_name = self.get_room_name(me_id, frnd_id)

#         # Send the message to the friend
#         await self.channel_layer.group_send(
#             room_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender': me_id,
#             }
#         )

#     async def chat_message(self, event):
#         # Called when a message is sent to the WebSocket
#         message = event['message']
#         sender = event['sender']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'sender': sender,
#         }))

#     @database_sync_to_async
#     def save_chat(self, me_id, frnd_id, message):
#         try:
#             me = MyUser.objects.get(id=me_id)
#             frnd = MyUser.objects.get(id=frnd_id)
#             mychats, _ = Mychats.objects.get_or_create(me=me, frnd=frnd)

#             # Append the new message to the existing chat
#             mychats.chats.append({'sender_id': me_id, 'message': message, 'timestamp': timezone.now().isoformat()})
#             mychats.save()
#         except MyUser.DoesNotExist:
#             pass

#     def get_room_name(self, me_id, frnd_id):
#         # Return a consistent room name by sorting the IDs
#         sorted_ids = sorted([me_id, frnd_id])
#         return f'chat_{sorted_ids[0]}_{sorted_ids[1]}'

from django.utils import timezone
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from api.models import MyUser, Mychats

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']  # User authenticated via JWT token

        if self.user and self.user.is_authenticated:
            self.user_id = self.user.id

            # Create a unique room for the user based on their own user ID
            self.room_group_name = f'user_{self.user_id}'

            # Add the user to their own group for direct messages
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close(code=4001)

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            # Remove the user from their own group on disconnect
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        me_id = self.user.id  # The sender is always the authenticated user
        frnd_id = int(data['frnd_id'])  # Recipient's ID is passed in the payload
        message = data['message']

        # Ensure room name is based on sorted user IDs to guarantee consistency
        room_name = self.get_room_name(me_id, frnd_id)

        # Save chat message to the database
        await self.save_chat(me_id, frnd_id, message)

        # Send the message to the group (shared between both users)
        await self.channel_layer.group_send(
            room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': me_id,
            }
        )

    async def chat_message(self, event):
        # Called when a message is sent to the WebSocket
        message = event['message']
        sender = event['sender']

        # Send the message to WebSocket clients
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))

    @database_sync_to_async
    def save_chat(self, me_id, frnd_id, message):
        try:
            # Ensure that messages between the same two users are saved in the same chat
            me = MyUser.objects.get(id=me_id)
            frnd = MyUser.objects.get(id=frnd_id)

            # Consistently save the chat by sorting the users
            sorted_users = sorted([me, frnd], key=lambda user: user.id)
            mychats, _ = Mychats.objects.get_or_create(me=sorted_users[0], frnd=sorted_users[1])

            # Append the new message to the existing chat
            mychats.chats.append({
                'sender_id': me_id,
                'message': message,
                'timestamp': timezone.now().isoformat()
            })
            mychats.save()
        except MyUser.DoesNotExist:
            pass

    def get_room_name(self, me_id, frnd_id):
        # Return a consistent room name by sorting the user IDs
        sorted_ids = sorted([me_id, frnd_id])
        return f'chat_{sorted_ids[0]}_{sorted_ids[1]}'

