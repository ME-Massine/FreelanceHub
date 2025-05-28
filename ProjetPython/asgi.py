import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing  # This imports websocket_urlpatterns from chat/routing.py
from django.core.asgi import get_asgi_application  # <-- FIXED import

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjetPython.settings')
django.setup()

application = ProtocolTypeRouter({
    # HTTP protocol handling
    "http": get_asgi_application(),  # <-- use the imported function directly

    # WebSocket protocol handling
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
