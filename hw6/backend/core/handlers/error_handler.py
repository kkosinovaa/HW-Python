# стандартний exception_handler з django rest framework.
# спочатку він обробляє звичайні drf помилки,
# а наш error_handler нижче додає окрему логіку для власних exception
from rest_framework.views import exception_handler


# Response потрібен, щоб вручну сформувати http-відповідь
# для нашої JWTException
from rest_framework.response import Response


# status містить готові http статус-коди.
# нижче використовуємо HTTP_401_UNAUTHORIZED,
# коли jwt токен неправильний або прострочений
from rest_framework import status


def error_handler(exc: Exception, context: dict):
    # словник зв'язує ім'я exception з функцією,
    # яка повинна обробити саме цю помилку.
    #
    # JWTException створюється в JWTService.verify_token()
    # через raise JWTException().
    # тут ми шукаємо її не через isinstance,
    # а по імені класу "JWTException"
    handlers = {
        'JWTException': _jwt_validation_exception_handler
    }

    # спочатку даємо стандартному drf handler
    # можливість обробити звичайні помилки,
    # наприклад validation error або permission error
    response = exception_handler(exc, context)

    # отримуємо назву класу помилки.
    # якщо exc це JWTException,
    # тут отримаємо рядок "JWTException"
    exc_class = exc.__class__.__name__

    # якщо для цієї помилки є наш окремий handler,
    # викликаємо його замість стандартної відповіді drf
    if exc_class in handlers:
        return handlers[exc_class](exc, context)

    # якщо це не наша спеціальна помилка,
    # повертаємо стандартну відповідь drf
    return response


def _jwt_validation_exception_handler(exc: Exception, context: dict):
    # цей handler викликається тільки для JWTException.
    #
    # сама JWTException виникає в JWTService.verify_token(),
    # коли токен неправильний, протермінований
    # або вже знаходиться в blacklist
    return Response(
        {
            'detail': 'JWT expired or invalid'
        },
        status=status.HTTP_401_UNAUTHORIZED
    )