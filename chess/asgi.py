"""
ASGI config for chess project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from chess_app.routing import ws_urlpatterns
from chess_app.consumers import GameConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chess.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            #[path(r"^game/$", GameConsumer.as_asgi()),]
            ws_urlpatterns
        )),
    
})