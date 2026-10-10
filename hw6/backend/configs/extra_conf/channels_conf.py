# налаштовуємо channel layer для websocket
CHANNEL_LAYERS = {
    "default": {
        # channels буде зберігати повідомлення і групи через redis
        "BACKEND": "channels_redis.core.RedisChannelLayer",

        # вказуємо адресу redis сервісу з docker-compose
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}