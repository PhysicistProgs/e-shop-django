from django.apps import AppConfig
from django.contrib import messages
from django.contrib.auth import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver


class StartedAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'started_app'

    def ready(self):
        from .models import User
        from cart.models import Cart

        @receiver(post_save, sender=User)
        def auto_create_cart(sender, instance, created, **kwargs):
            if created:
                Cart.objects.create(owner=instance)

        @receiver(user_logged_in, sender=User)
        def add_from_session(sender, request, user, **kwargs):
            from .models import Shoe
            if 'cart' in request.session:
                for key in request.session['cart'].keys():
                    added = Shoe.objects.get(pk=int(key))
                    quantity = request.session['cart'][key]['quantity']
                    user.cart.products.add(added, through_defaults={'quantity': quantity})
                    messages.success(request, 'Мы добавили в вашу корзину товары')
