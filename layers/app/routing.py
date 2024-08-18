from django.urls import path
from .consumers import MySyncConsumer,MyAsyncConsumer,MyWebsocketConsumer,MyAsyncWebsocketConsumer


websocket_urlpatterns = [
    path('ws/sc/<str:groupkaname>/', MySyncConsumer.as_asgi()),
    path('ws/ac/<str:groupkaname>/', MyAsyncConsumer.as_asgi()),
    path('ws/wsc/',MyWebsocketConsumer.as_asgi()),
    path('ws/wsac/',MyAsyncWebsocketConsumer.as_asgi())

    
]