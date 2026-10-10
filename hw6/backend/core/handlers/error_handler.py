from rest_framework.response import Response
from rest_framework.views import exception_handler


def error_handler(exc: Exception, context: dict):
    # тут вказуємо яку помилку яким handler-ом обробляти
    handlers = {
        "JWTException": _jwt_validation_exception_handler
    }

    # стандартний handler drf обробляє всі звичайні помилки
    response = exception_handler(exc, context)

    # отримуємо назву класу помилки
    exc_class = exc.__class__.__name__

    # якщо для цієї помилки є наш handler, викликаємо його
    if exc_class in handlers:
        return handlers[exc_class](exc, context)

    # якщо окремого handler-а нема, повертаємо стандартну відповідь drf
    return response


def _jwt_validation_exception_handler(exc: Exception, context: dict):
    # для проблем з jwt повертаємо 401
    return Response(
        {'detail': 'JWT expired or invalid'},
        status=401
    )