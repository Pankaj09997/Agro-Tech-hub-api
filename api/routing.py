from django.urls import path
from api.consumers import MychatApp

websocket_urlpatterns =[

    path('ws/wsc/<int:pk>',MychatApp.as_asgi())
]