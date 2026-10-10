from .jwt_conf import *
from .rest_conf import *
from .email_conf import *

# підтягуємо налаштування celery в основні settings django
from .celery_conf import *