from cart.models import CartProducts
from started_app.utils import DataMixin


class CartMixin(DataMixin):

    def get_user_context(self, **kwargs):
        context = super().get_user_context(**kwargs)
        if self.request.user.is_authenticated:
            context['quantity'] = {}
        return context
