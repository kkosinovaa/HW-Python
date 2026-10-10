# імпортуємо celery app, щоб він завантажувався разом з django
from .celery import app as celery_app

# вказуємо, що celery_app доступний при імпорті пакета configs
__all__ = ['celery_app']