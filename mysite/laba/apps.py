from django.apps import AppConfig

class LabaConfig(AppConfig):
    name = 'laba'

    def ready(self):
        import laba.signals