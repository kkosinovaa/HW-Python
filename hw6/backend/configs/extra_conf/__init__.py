from .jwt_conf import *
from .rest_conf import *
from .email_conf import *

# імпортуємо всі налаштування celery з celery_conf.py
# у пакет configs.extra_conf.
#
# далі settings.py виконує:
# from .extra_conf import *
# тому змінні CELERY_* з цього файла стають частиною django settings.
#
# після цього configs/celery.py читає їх через
# app.config_from_object('django.conf:settings', namespace='CELERY')
from .celery_conf import *