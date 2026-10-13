# Type потрібен для типізації класів токенів.
# нижче через Type[ActionToken] ми вказуємо, що в методи сервісу
# передається не готовий об'єкт токена, а сам клас токена,
# наприклад ActivateToken або RecoveryToken
from typing import Type


# get_user_model повертає ту модель користувача,
# яка вказана в django settings як AUTH_USER_MODEL.
# це краще, ніж напряму імпортувати конкретну модель,
# тому що код не залежить від її точного розташування
from django.contrib.auth import get_user_model


# get_object_or_404 шукає об'єкт у базі даних.
# якщо користувача з таким id немає,
# django автоматично поверне помилку 404
from rest_framework.generics import get_object_or_404


# ActionTokenEnum містить налаштування наших action token:
# тип токена і час його життя.
# нижче ці значення використовуються в ActivateToken і RecoveryToken
from core.enums.action_token_enum import ActionTokenEnum


# JWTException це наша власна помилка для проблем з jwt токеном.
# вона викликається нижче в verify_token(),
# а потім глобальний error_handler визначає її по імені класу
# "JWTException" і повертає відповідь зі статусом 401
from core.exceptions.jwt_exception import JWTException


# BlacklistMixin додає токенам підтримку blacklist,
# тобто можливість перевірити, чи токен вже був використаний,
# і додати його в blacklist після використання.
#
# Token це базовий клас simplejwt,
# на основі якого створюються наші власні типи токенів
from rest_framework_simplejwt.tokens import BlacklistMixin, Token


# отримуємо модель користувача, яка використовується в цьому проєкті.
# нижче UserModel передається в get_object_or_404(),
# щоб знайти користувача по user_id з jwt токена
UserModel = get_user_model()


# окремий базовий клас токена з підтримкою blacklist.
# він може використовуватися для токенів,
# які повинні ставати недійсними після використання
class BlacklistToken(BlacklistMixin, Token):
    pass


# ActionToken це базовий клас для наших спеціальних токенів,
# наприклад токена активації акаунта або відновлення пароля.
#
# BlacklistMixin потрібен, щоб такі токени були одноразовими:
# після успішної перевірки verify_token() додає їх у blacklist
class ActionToken(BlacklistMixin, Token):
    pass


# цей тип означає "клас, який успадковується від ActionToken".
# він використовується в create_token() і verify_token(),
# щоб один і той самий код міг працювати з різними типами action token
ActionTokenClassType = Type[ActionToken]


# токен для активації акаунта.
# тип токена і час життя не прописуємо тут вручну,
# а беремо з ActionTokenEnum.ACTIVATE
class ActivateToken(ActionToken):
    token_type = ActionTokenEnum.ACTIVATE.token_type
    lifetime = ActionTokenEnum.ACTIVATE.lifetime


# токен для відновлення пароля.
# він працює за тим самим принципом,
# але має свій token_type і lifetime з ActionTokenEnum.RECOVERY
class RecoveryToken(ActionToken):
    token_type = ActionTokenEnum.RECOVERY.token_type
    lifetime = ActionTokenEnum.RECOVERY.lifetime


# сервіс, який містить спільну логіку створення
# і перевірки наших action token.
# завдяки цьому ця логіка не дублюється у views
class JWTService:

    @staticmethod
    def create_token(user, token_class: ActionTokenClassType):
        # token_class передається з view.
        # це може бути, наприклад, ActivateToken або RecoveryToken.
        #
        # for_user(user) створює jwt для конкретного користувача
        # і записує його user_id у payload токена.
        #
        # створений token потім можна передати користувачу,
        # наприклад у листі активації або відновлення пароля
        return token_class.for_user(user)

    @staticmethod
    def verify_token(token, token_class: ActionTokenClassType):
        # цей метод викликається з auth views,
        # коли треба перевірити action token,
        # наприклад токен активації або recovery token
        try:
            # створюємо об'єкт потрібного типу токена
            # з отриманого рядка token.
            #
            # token_class визначає, який саме тип токена очікується.
            # якщо передали ActivateToken, то recovery token
            # не повинен пройти як правильний activate token
            token_res = token_class(token)

            # перевіряємо, чи токен ще не знаходиться в blacklist.
            # якщо він вже був використаний раніше,
            # simplejwt згенерує помилку
            token_res.check_blacklist()

        except Exception:
            # сюди потрапляємо, якщо токен неправильний,
            # прострочений, вже знаходиться в blacklist
            # або його взагалі неможливо розібрати.
            #
            # замість того щоб повертати різні помилки simplejwt,
            # кидаємо одну нашу JWTException.
            #
            # далі django rest framework передає її
            # у глобальний error_handler.
            # error_handler бере exc.__class__.__name__,
            # отримує рядок "JWTException",
            # знаходить його у словнику handlers
            # і викликає окремий jwt handler,
            # який повертає відповідь 401
            raise JWTException()

        # якщо перевірка пройшла успішно,
        # додаємо токен у blacklist.
        # через це action token стає одноразовим
        # і повторно використати його вже не вийде
        token_res.blacklist()

        # під час створення токена через for_user()
        # у payload був записаний user_id.
        # тут дістаємо його назад,
        # щоб зрозуміти, для якого користувача був створений токен
        user_id = token_res.payload.get('user_id')

        # шукаємо користувача в базі по user_id.
        # повернений UserModel далі використовує view,
        # наприклад для активації акаунта
        # або зміни пароля при recovery.
        #
        # якщо такого користувача немає,
        # get_object_or_404 автоматично поверне 404
        return get_object_or_404(UserModel, pk=user_id)