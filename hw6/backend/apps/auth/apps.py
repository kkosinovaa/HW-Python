from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'apps.auth'
    label = 'auth_' #внутрішня назва щоб не було конфлікту
