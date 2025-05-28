from django.urls import path
from . import consumers  # Import consumers from chat app

websocket_urlpatterns = [
    path("ws/chat/<str:room_name>/", consumers.ChatConsumer.as_asgi()),
]
