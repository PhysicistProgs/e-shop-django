from django.contrib.auth.models import User
from .models import Shoe, Material, Brand


class DataMixin:
    filters = {'brand', 'material', 'brand_country', 'price'}

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

    def get_str_materials(self):
        return [str(i) for i in Material.objects.all()]

    def get_str_brands(self):
        return [str(i) for i in Brand.objects.all()]

    def get_str_brands_coutry(self):
        return [str(i.country) for i in Brand.objects.all()]

    def getrequest_material(self):
        return self.request.GET.getlist('material')

    def getrequest_brand(self):
        return self.request.GET.getlist('brand')

    def getrequest_price_up(self):
        price = self.request.GET.getlist('price-up-to')[0]
        return price

    def getrequest_price_from(self):
        price = self.request.GET.getlist('price-from')[0]
        return price

