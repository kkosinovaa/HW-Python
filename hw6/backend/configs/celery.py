# os потрібен для роботи зі змінними середовища.
# тут через нього ми вказуємо celery, який файл django settings треба використовувати
import os

# Celery це головний клас, з якого створюється celery app.
# цей app потім використовується для реєстрації і запуску фонових задач
from celery import Celery

# crontab потрібен нижче в beat_schedule для задання періодичності задач
from celery.schedules import crontab


# спочатку вказуємо модуль налаштувань django.
# цей рядок має бути ДО Celery(...), тому що celery під час створення app
# вже повинен знати, де знаходяться налаштування django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')


# створюємо головний celery app.
# цей app далі імпортується в configs/__init__.py,
# а також у core/services/email_service.py, де через @app.task
# методи реєструються як задачі celery
app = Celery('settings')


# celery бере свої налаштування з django settings.
# namespace='CELERY' означає, що celery шукає тільки параметри
# з префіксом CELERY_, наприклад CELERY_BROKER_URL,
# CELERY_RESULT_BACKEND, CELERY_TASK_SERIALIZER.
# самі ці параметри знаходяться в configs/extra_conf/celery_conf.py
# і через django settings стають доступними celery
app.config_from_object('django.conf:settings', namespace='CELERY')


# автоматично шукає celery-задачі в django застосунках,
# тому не потрібно вручну реєструвати кожну задачу окремо
app.autodiscover_tasks()


# beat_schedule описує періодичні задачі celery beat.
# task це повний шлях до задачі spam з email_service.py.
# crontab() без параметрів означає запуск кожну хвилину.
# celery beat читає цей розклад, а celery worker вже виконує саму задачу
app.conf.beat_schedule = {
    'send_spam_every_minutes': {
        'task': 'core.services.email_service.spam',
        'schedule': crontab(),
        # тут були б аргументи задачі, якби spam приймав параметри
        # 'args': (),
    }
}