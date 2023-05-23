from django.apps import AppConfig


class RafacarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rafacar'


class RafaCarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rafacar'

    def ready(self):
        import rafacar.signals
