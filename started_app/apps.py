from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver


class StartedAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'started_app'

    def ready(self):
        from .models import User, Cart

        @receiver(post_save, sender=User)
        def auto_create_cart(sender, instance, created, **kwargs):
            if created:
                Cart.objects.create(owner=instance)
