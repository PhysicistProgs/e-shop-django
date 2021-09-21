from django.contrib.auth.models import User


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        products = self.request.user.cart.products.all()
        cart_number = len(products)
        context['cart_number'] = cart_number
        return context
