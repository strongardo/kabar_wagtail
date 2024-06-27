from django.apps import AppConfig


class SimplePagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simple_pages'

    def ready(self):
        import simple_pages.signals
