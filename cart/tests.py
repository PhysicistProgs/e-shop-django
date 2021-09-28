from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from .models import CartProducts, Cart
from started_app.models import Shoe


class CartProductsModelTest(TestCase):
    def cart_products_test(self):
        """
        return error if in CartProducts model there is more
        more then one line when filtering by shoe and cart
        simultaneously
        """
        shoes = Shoe.objects.all()
        users = User.objects.all()
        error = False

        for shoe in shoes:
            for user in users:
                if CartProducts.objects.filter(shoe=shoe, cart=user.cart) > 1:
                    error = True
        self.assertIs(error, False)
