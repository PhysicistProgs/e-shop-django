from cart.models import CartProducts
from started_app.utils import DataMixin


class CartMixin(DataMixin):

    def get_user_context(self, **kwargs):
        context = super().get_user_context(**kwargs)
        if self.request.user.is_authenticated:
            products = context['products_for_cart_view']
            context['quantity'] = {}
            for item in products:
                context['quantity'][item.pk] = item.cartproducts_set.get(
                    cart=self.request.user.cart
                ).quantity
            context.pop('products_for_cart_view')
        return context
