# імпортуємо celery app, який створюється в configs/celery.py.
# завдяки цьому при завантаженні пакета configs
# celery app також створюється і отримує django settings.
#
# сам app далі використовується в core/services/email_service.py,
# де через @app.task реєструються фонові задачі
from .celery import app as celery_app


# вказуємо, що celery_app є публічним об'єктом цього пакета.
# це дозволяє явно експортувати celery app з configs
__all__ = ('celery_app',)