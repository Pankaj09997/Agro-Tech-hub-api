# api/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path(r'ws/chat/(?P<conversation_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
    ]