"""
ASGI config for fido_web project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import messages.routing
import notifications.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fido_web.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(
                notifications.routing.websocket_urlpatterns
                + messages.routing.websocket_urlpatterns
            )
        ),
    }
)
