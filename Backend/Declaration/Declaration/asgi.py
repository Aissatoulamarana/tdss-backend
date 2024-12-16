import os
from django.core.asgi import get_asgi_application
from django.urls import re_path, path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django_nextjs.proxy import NextJSProxyHttpConsumer, NextJSProxyWebsocketConsumer
from django.conf import settings
from .consumers import DeclarationConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Declaration.settings')

# Récupération de l'application ASGI
application = get_asgi_application()

# Définir les routes HTTP et WebSocket
http_routes = [re_path(r"", application)]  # Utilisez 'application' ici, pas 'django_asgi_app'
websocket_routers = []

# Configuration des routes Next.js pour le mode DEBUG
if settings.DEBUG:
    # Route pour les requêtes HTTP Next.js
    http_routes.insert(0, re_path(r"^(?:_next|__next|next).*", NextJSProxyHttpConsumer.as_asgi()))
    
    # Route WebSocket pour la gestion de HMR (Hot Module Replacement) Next.js
    websocket_routers.insert(0, path("_next/webpack-hmr", NextJSProxyWebsocketConsumer.as_asgi()))

    websocket_routers.append(
    path('ws/declarations/', DeclarationConsumer.as_asgi())
)

# Application du routage pour HTTP et WebSocket
application = ProtocolTypeRouter(
    {
        "http": URLRouter(http_routes),
        "websocket": AuthMiddlewareStack(URLRouter(websocket_routers)),
        # Ajoutez d'autres protocoles ici si nécessaire
    }
)
