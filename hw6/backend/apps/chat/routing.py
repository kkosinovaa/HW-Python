from django.urls import path

from .consumers import ChatConsumer


# тут зберігаються websocket маршрути для chat
websocket_urlpatterns = [
    # room буде назвою кімнати, до якої підключається користувач
    path('<str:room>/', ChatConsumer.as_asgi())
]