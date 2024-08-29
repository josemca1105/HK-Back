from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hk_back.users'

    def ready(self):
        import hk_back.users.signals
