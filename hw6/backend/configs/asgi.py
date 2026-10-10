import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

from configs.routing import websocket_urlpatterns
from core.middleware.socket_middleware import AuthSocketMiddleware


# вказуємо django, де знаходяться основні налаштування
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')

# розділяємо звичайні http запити і websocket підключення
application = ProtocolTypeRouter({
    # звичайні http запити працюють через стандартний django asgi application
    'http': get_asgi_application(),

    # websocket спочатку проходить через наш middleware для авторизації
    'websocket': AuthSocketMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})