import os

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from configs.celery import app
from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken


UserModel = get_user_model()


class EmailService:

    # позначаємо функцію як задачу celery
    @app.task
    def __send_email(to: str, template_name: str, context: dict, subject: str) -> None:
        # беремо потрібний html шаблон
        template = get_template(template_name)

        # передаємо дані в шаблон
        html_content = template.render(context)

        # створюємо лист
        msg = EmailMultiAlternatives(
            to=[to],
            from_email=os.environ.get('EMAIL_HOST_USER'),
            subject=subject
        )

        # додаємо html до листа
        msg.attach_alternative(html_content, "text/html")

        # відправляємо лист
        msg.send()

    @classmethod
    def register(cls, user):
        # створюємо токен для активації користувача
        token = JWTService.create_token(user, ActivateToken)

        # створюємо посилання для активації
        url = f'http://localhost/activate/{token}'

        # delay передає відправку листа celery
        cls.__send_email.delay(
            to=user.email,
            template_name='register.html',
            context={'name': user.profile.name, 'url': url},
            subject="Register"
        )

    @classmethod
    def recovery(cls, user):
        # створюємо токен для відновлення пароля
        token = JWTService.create_token(user, RecoveryToken)

        # створюємо посилання для зміни пароля
        url = f'http://localhost/api/auth/recovery/{token}'

        # відправку recovery листа теж передаємо celery
        cls.__send_email.delay(
            to=user.email,
            template_name='recovery.html',
            context={'url': url},
            subject="Recovery"
        )

    @staticmethod
    @app.task
    def spam():
        # перебираємо всіх користувачів
        for user in UserModel.objects.all():

            # spam вже виконується celery, тому тут просто викликаємо відправку листа
            EmailService.__send_email(
                user.email,
                'spam.html',
                {},
                'SPAM'
            )