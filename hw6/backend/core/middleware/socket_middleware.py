from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from core.services.jwt_service import JWTService, SocketToken


# ця функція шукає користувача за socket token
@database_sync_to_async
def get_user(token: str | None):
    try:
        return JWTService.verify_token(token, SocketToken)
    except (Exception,):
        pass


# цей middleware відповідає за авторизацію користувача під час websocket підключення
class AuthSocketMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # декодуємо query string і дістаємо з нього token
        token = dict(
            [
                item.split('=')
                for item in scope['query_string'].decode('utf-8').split('&')
                if item
            ]
        ).get('token', None)

        # дивимось який token прийшов
        print('TOKEN:', token)

        # знаходимо користувача за token і записуємо його в scope
        scope['user'] = await get_user(token=token)

        # дивимось якого користувача знайшли
        print('USER:', scope['user'])

        # передаємо websocket підключення далі
        return await super().__call__(scope, receive, send)