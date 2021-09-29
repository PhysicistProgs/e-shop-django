from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from started_app.models import Shoe


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


class PaymentMethod(models.Model):
    """
    Payment method for Order model
    """
    CASH = ("CS", "Cash")
    BANK_CARD = ("CD", "Bank Card")
    APPLEPAY = ("AP", "Apple Pay")
    __all = dict([CASH, BANK_CARD, APPLEPAY])

    method = models.CharField(max_length=2, choices=__all.items())

    def __str__(self):
        return self.__all[self.method]


class Order(models.Model):
    """
    Order model. ManyToMany relationship with Shoes model
    and ManyToOne with Client model.
    """
    # Linking
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    shoes = models.ManyToManyField(Shoe, through='OrderProduct')

    # Business logic
    CANCELED = 0
    PROCESSING = 1
    PREPARING = 2
    DELIVERING = 3
    DONE = 4

    STATUS_CHOICES = [
        (CANCELED, 'Canceled'),
        (PROCESSING, 'Processing'),
        (PREPARING, 'Preparing'),
        (DELIVERING, 'Delivered'),
        (DONE, 'Done')
    ]

    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PROCESSING)
    comment = models.CharField(max_length=300, blank=True)

    # Utils
    date_created = models.DateField(default=timezone.now, auto_created=True, null=False)

    # date_delivered = models.DateField(default=None, auto_created=True, null=True)
    # delivered = models.DateField(default=False, null=False)

    # def __str__(self):
    #     return "name: {}, comment: {}, order id: {}".format(self.user_id.name, self.comment, self.pk)

    def mark_delivered(self, commit=True):
        self.delivered = True
        self.date_delivered = timezone.now()
        self.status = self.DONE
        if commit:
            self.save()


class OrderProduct(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)
    price = models.IntegerField(null=True)
