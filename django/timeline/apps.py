from django.apps import AppConfig
from django.db.models.signals import post_migrate


class TimelineConfig(AppConfig):
    name = 'timeline'

    def ready(self):
        from .models import create_default_category
        post_migrate.connect(create_default_category, sender=self)
