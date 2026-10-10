from typing import cast

from channels.db import database_sync_to_async
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer


class ChatConsumer(GenericAsyncAPIConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # тут зберігаємо назву кімнати
        self.room_name = None

        # тут зберігаємо ім'я користувача
        self.user_name = None

    async def connect(self):
        # якщо користувач не авторизований, закриваємо websocket
        if not self.scope['user']:
            return await self.close()

        # приймаємо websocket підключення
        await self.accept()

        # дістаємо назву кімнати з url
        self.room_name = cast(
            str,
            self.scope['url_route']['kwargs'].get('room')
        )

        # отримуємо ім'я користувача
        self.user_name = await self.get_profile_name()

        # додаємо користувача до групи кімнати
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        # після підключення відправляємо повідомлення всім у кімнаті
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'sender',
                'message': f'{self.user_name} connected to chat'
            }
        )

    async def sender(self, data):
        # виводимо повідомлення в консоль
        print(data)

        # відправляємо повідомлення клієнту
        await self.send_json(data)

    @action()
    async def send_message(self, data, request_id, action):
        # відправляємо повідомлення всім користувачам у кімнаті
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'sender',
                'message': data,
                'user': self.user_name,
                'id': request_id
            }
        )

    @database_sync_to_async
    def get_profile_name(self):
        # дістаємо користувача з websocket scope
        user = self.scope['user']

        # виводимо користувача в консоль
        print('USER:', user)

        # повертаємо ім'я з профілю
        return user.profile.name