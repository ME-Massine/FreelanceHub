import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application  # Keep this above django.setup()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjetPython.settings')
django.setup()  # ✅ Run this before importing anything that touches models/apps

import chat.routing  # ✅ Now it's safe to import

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
