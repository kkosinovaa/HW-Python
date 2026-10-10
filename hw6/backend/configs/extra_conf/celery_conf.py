# адреса redis, через який django передає задачі celery
CELERY_BROKER_URL = 'redis://redis:6379/0'

# результати виконання задач зберігаємо в базі даних django
CELERY_RESULT_BACKEND = 'django-db'

# celery приймає дані задач у форматі json
CELERY_ACCEPT_CONTENT = ['application/json']

# задачі перед відправкою серіалізуються в json
CELERY_TASK_SERIALIZER = 'json'

# результат виконання задач теж зберігається у форматі json
CELERY_RESULT_SERIALIZER = 'json'

# scheduler для періодичних задач через django-celery-beat
#CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'