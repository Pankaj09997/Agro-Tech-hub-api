# api/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json

class MySyncConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print('WebSocket Connect ...')

    def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # print(text_data)
        # message = text_data_json['message']
        # print(message)
        print('Message received from client', text_data)
        # print("Name of the layer is:",self.channel_layer)
        # print("name of the channel is:",self.channel_name)
        

        
        self.send(text_data=json.dumps({
            'message': 'Message sent to client from application'
        }))
    
    def disconnect(self, close_code):
        print('WebSocket Disconnected...', close_code)
 