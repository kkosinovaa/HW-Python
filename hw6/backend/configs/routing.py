from django.urls import path

from channels.routing import URLRouter

from apps.chat.routing import websocket_urlpatterns as chat_routing


# підключаємо websocket маршрути з chat до загального роутингу
websocket_urlpatterns = [
    path('api/chat/', URLRouter(chat_routing))
]