

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack




os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'layers.settings')
django.setup()

from app.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
            ),
})