from django.contrib.auth.models import User
from django.db.models import QuerySet
import json


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        if self.request.user.is_authenticated:
            products = self.request.user.cart.products.all()
            cart_number = len(products)
        else:
            if 'cart' not in self.request.session:
                self.request.session['cart'] = {}
            cart = self.request.session['cart']
            cart_number = len(cart)
        context['cart_number'] = cart_number
        return context
