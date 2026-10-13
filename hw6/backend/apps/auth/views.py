# get_user_model повертає модель користувача,
# яка вказана в django settings як AUTH_USER_MODEL.
# нижче через неї створюємо UserModel,
# який використовується в RecoveryRequestView для пошуку користувача по email
from django.contrib.auth import get_user_model


# status містить стандартні http статус-коди.
# нижче використовуємо HTTP_200_OK для успішних відповідей
from rest_framework import status


# GenericAPIView є базовим класом для наших auth views.
# get_object_or_404 використовується нижче в RecoveryRequestView:
# він шукає користувача по email і автоматично повертає 404,
# якщо такого користувача в базі немає
from rest_framework.generics import GenericAPIView, get_object_or_404


# AllowAny дозволяє звертатися до цих endpoint без авторизації.
# це потрібно, тому що користувач під час активації або recovery
# ще може не мати access token
from rest_framework.permissions import AllowAny


# Response формує http-відповідь,
# яку кожен view повертає клієнту після виконання операції
from rest_framework.response import Response


# EmailService містить логіку відправки email.
# у RecoveryRequestView він використовується для запуску
# відправки листа для відновлення пароля
from core.services.email_service import EmailService


# JWTService містить спільну логіку створення і перевірки action token.
#
# ActivateToken використовується в ActivateUserView,
# тому там очікується саме токен активації акаунта.
#
# RecoveryToken використовується в RecoveryPasswordView,
# тому там очікується саме токен відновлення пароля
from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken


# EmailSerializer перевіряє email,
# який користувач надсилає для запиту на відновлення пароля.
#
# PasswordSerializer перевіряє новий пароль,
# який користувач надсилає після переходу по recovery link
from apps.auth.serializers import EmailSerializer, PasswordSerializer


# UserSerializer перетворює об'єкт користувача у дані,
# які можна повернути клієнту у Response.
# нижче використовується після успішної активації акаунта
from apps.user.serializers import UserSerializer


# отримуємо модель користувача з django settings.
# нижче вона використовується в RecoveryRequestView
# для пошуку користувача по email
UserModel = get_user_model()


# view для активації акаунта користувача
class ActivateUserView(GenericAPIView):

    # endpoint доступний без access token,
    # тому що користувач активує акаунт через action token з посилання
    permission_classes = (AllowAny,)

    def patch(self, *args, **kwargs):

        # token приходить у url і передається у kwargs.
        # це саме токен активації, який користувач отримав раніше
        token = kwargs['token']

        # викликаємо спільний JWTService.verify_token().
        # другим аргументом передаємо ActivateToken,
        # тому сервіс очікує саме токен активації.
        #
        # verify_token() перевіряє токен і blacklist,
        # після чого дістає user_id з payload
        # і повертає відповідного користувача з бази.
        #
        # якщо токен неправильний, прострочений або вже використаний,
        # всередині verify_token() викликається raise JWTException().
        # далі глобальний error_handler знаходить помилку
        # по імені класу "JWTException"
        # і повертає клієнту 401
        user = JWTService.verify_token(token, ActivateToken)

        # після успішної перевірки токена
        # активуємо акаунт користувача
        user.is_active = True

        # зберігаємо зміну is_active у базі даних
        user.save()

        # перетворюємо модель користувача у дані,
        # які можна повернути клієнту у json
        serializer = UserSerializer(user)

        # повертаємо дані активованого користувача
        # і статус успішного виконання 200
        return Response(serializer.data, status.HTTP_200_OK)


# view для першого етапу відновлення пароля:
# користувач надсилає свій email,
# після чого йому відправляється recovery link
class RecoveryRequestView(GenericAPIView):

    # користувач ще не авторизований,
    # тому endpoint доступний для всіх
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):

        # отримуємо дані, які клієнт передав у body request
        data = request.data

        # передаємо отримані дані в EmailSerializer,
        # щоб перевірити правильність email
        serializer = EmailSerializer(data=data)

        # запускаємо валідацію.
        # якщо email не пройде перевірку,
        # drf автоматично поверне помилку валідації
        serializer.is_valid(raise_exception=True)

        # беремо вже перевірений email з validated_data
        # і шукаємо користувача з таким email у базі.
        #
        # UserModel був отриманий вище через get_user_model().
        # якщо користувача з таким email немає,
        # get_object_or_404 автоматично поверне 404
        user = get_object_or_404(
            UserModel,
            email=serializer.validated_data['email']
        )

        # передаємо знайденого користувача в EmailService.
        # сервіс відповідає за підготовку і відправку
        # листа для відновлення пароля
        EmailService.recovery(user)

        # повідомляємо клієнту, що посилання
        # для відновлення пароля було відправлено на email
        return Response(
            {'details': 'link send to email'},
            status.HTTP_200_OK
        )


# view для другого етапу recovery:
# користувач уже має recovery token
# і надсилає новий пароль
class RecoveryPasswordView(GenericAPIView):

    # access token тут не потрібен,
    # тому що право на зміну пароля підтверджується recovery token
    permission_classes = (AllowAny,)

    def post(self, *args, **kwargs):

        # отримуємо новий пароль з body request
        data = self.request.data

        # PasswordSerializer перевіряє отриманий пароль
        # відповідно до логіки serializer
        serializer = PasswordSerializer(data=data)

        # запускаємо валідацію.
        # якщо пароль неправильний,
        # drf автоматично поверне помилку
        serializer.is_valid(raise_exception=True)

        # recovery token приходить через url
        # і доступний у kwargs
        token = kwargs['token']

        # перевіряємо token через JWTService.verify_token(),
        # але цього разу передаємо RecoveryToken.
        # це означає, що очікується саме токен відновлення пароля.
        #
        # якщо токен правильний, verify_token()
        # повертає користувача, для якого він був створений.
        #
        # якщо токен неправильний, прострочений або вже використаний,
        # verify_token() викликає JWTException.
        # далі error_handler ловить її по імені класу
        # і повертає клієнту 401
        user = JWTService.verify_token(token, RecoveryToken)

        # set_password не просто записує текст пароля,
        # а правильно хешує його перед збереженням у базу
        user.set_password(serializer.validated_data['password'])

        # зберігаємо новий хеш пароля користувача в базі
        user.save()

        # якщо пароль успішно змінено,
        # повертаємо статус 200
        return Response(status=status.HTTP_200_OK)