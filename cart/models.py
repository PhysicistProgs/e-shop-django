from django.db import models
from django.contrib.auth.models import User
from started_app.models import Shoe, Order


class Cart(models.Model):
    """
    Store current cart. Only one cart for one user is available.
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Shoe, blank=True, through='CartProducts')


class CartProducts(models.Model):
    """
    Tight Cart and Shoe models and add quantity of exact shoe
    in user's cart
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.cart) + str(self.shoe.name) + str(self.quantity)