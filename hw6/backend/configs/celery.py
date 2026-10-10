# цей файл створює головний об'єкт celery app
import os

from celery import Celery
from celery.schedules import crontab


# вказуємо де celery брати налаштування django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')

# створюємо головний об'єкт celery
app = Celery('settings')

# підтягуємо налаштування celery з django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# шукаємо celery-задачі в django-застосунках
app.autodiscover_tasks()

# тут налаштовуємо періодичні задачі
app.conf.beat_schedule = {
    'send_spam_every_minutes': {
        # шлях до задачі, яку треба запускати
        'task': 'core.services.email_service.spam',

        # crontab без параметрів означає запуск кожну хвилину
        'schedule': crontab(),

        # якщо задача приймає аргументи, їх можна передати через args
        # 'args': (),
    }
}