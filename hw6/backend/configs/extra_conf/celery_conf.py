# broker це посередник між django і celery worker.
# коли django створює задачу, вона потрапляє в redis,
# а celery worker забирає її звідти і виконує
# redis тут це не localhost, а назва сервісу redis з docker-compose.yml,
# тому контейнери можуть звертатися один до одного по цій назві
CELERY_BROKER_URL = 'redis://redis:6379/0'


# сюди celery зберігає результат виконання задач
# django-db означає, що результати зберігаються в базі django
# для цього використовується пакет django-celery-results
CELERY_RESULT_BACKEND = 'django-db'


# задачі перед відправкою в broker серіалізуються у json
# це визначає формат даних, які celery передає через redis
CELERY_TASK_SERIALIZER = 'json'


# результат задачі celery теж повертає у форматі json
CELERY_RESULT_SERIALIZER = 'json'


# дозволяємо celery приймати повідомлення тільки у форматі json
# це має відповідати CELERY_TASK_SERIALIZER
CELERY_ACCEPT_CONTENT = ['json']


# цей scheduler зберігає розклад celery beat у базі django
# він використовується для періодичних задач
# і пов'язаний з django-celery-beat
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'