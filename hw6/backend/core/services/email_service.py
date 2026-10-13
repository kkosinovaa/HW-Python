# render_to_string бере html-шаблон і підставляє в нього дані,
# після чого повертає готовий html-текст листа
from django.template.loader import render_to_string

# EmailMultiAlternatives використовується для створення і відправки email,
# у тому числі html-версії листа
from django.core.mail import EmailMultiAlternatives

# UserModel це наша модель користувача.
# нижче вона використовується в spam(), щоб отримати всіх користувачів
# і відправити лист кожному з них
from apps.user.models import UserModel

# app це celery app, створений у configs/celery.py.
# тут він потрібен для декоратора @app.task,
# який реєструє метод як celery-задачу
from configs.celery import app


class EmailService:

    @staticmethod
    def __send_email(to: str, template_name: str, context: dict, subject: str):
        # render_to_string формує html листа з шаблону
        # template_name вказує, який шаблон використати,
        # а context містить дані, які підставляються в шаблон
        html_content = render_to_string(template_name, context)

        # створюємо email-повідомлення.
        # subject це тема листа, to це список отримувачів
        email = EmailMultiAlternatives(
            subject=subject,
            body='',
            to=[to]
        )

        # додаємо html-версію листа,
        # щоб поштовий клієнт відобразив готову html-сторінку
        email.attach_alternative(html_content, 'text/html')

        # фактично відправляємо email через налаштований django email backend
        email.send()


    @staticmethod
    @app.task
    def register(user_id: int, token: str):
        # @app.task робить цей метод celery-задачею,
        # тому він може виконуватися не в django request,
        # а окремим celery worker

        # отримуємо користувача з бази по id,
        # бо в celery-задачу краще передавати прості дані,
        # а не сам django model object
        user = UserModel.objects.get(pk=user_id)

        # викликаємо спільний метод відправки листа
        # і передаємо email користувача та token у шаблон
        EmailService.__send_email(
            user.email,
            'register.html',
            {'token': token},
            'Activate account'
        )


    @staticmethod
    @app.task
    def recovery(user_id: int, token: str):
        # ця задача працює так само через celery worker,
        # але використовується для відновлення пароля

        # знаходимо користувача в базі по id,
        # який передали під час створення задачі
        user = UserModel.objects.get(pk=user_id)

        # передаємо recovery token у шаблон листа
        EmailService.__send_email(
            user.email,
            'recovery.html',
            {'token': token},
            'Recovery password'
        )


    @staticmethod
    @app.task
    def spam():
        # UserModel.objects.all() отримує всіх користувачів з бази,
        # щоб задача могла пройтись по кожному користувачу
        for user in UserModel.objects.all():

            # кожному користувачу відправляється однаковий spam лист
            EmailService.__send_email(
                user.email,
                'spam.html',
                {},
                'SPAM'
            )