from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Brand(models.Model):
    """
    Brand for Shoe model. One to many link.
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    country = models.CharField(max_length=30, blank=True)
    logo = models.ImageField()

    def __str__(self):
        return str(self.name)


class Material(models.Model):
    """
    Material for Shoe model. One to many link.
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Shoe(models.Model):
    """
    Shoe model.
    """
    # Linking
    material_id = models.ForeignKey(Material, null=False, on_delete=models.CASCADE)
    brand_id = models.ForeignKey(Brand, null=False, on_delete=models.CASCADE)

    # Business logic
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    price = models.IntegerField(null=False)
    is_available = models.BooleanField(default=False)

    # SEO
    SEO_keywords = models.CharField(max_length=255)
    SEO_description = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class ShoeImage(models.Model):
    """
    Images for Shoe model. Many to many link
    """
    shoe_id = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    image = models.ImageField()


class Category(models.Model):
    """
    Category for Shoe model. Many to many link
    """
    # Linking
    shoe_id = models.ManyToManyField(Shoe)
    # Business logic
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    image = models.ImageField()
    is_available = models.BooleanField()


class Size(models.Model):
    SIZE_CHOICES = [
        (35, '35'),
        (36, '36'),
        (37, '37'),
        (38, '38'),
        (39, '39'),
        (40, '40'),
        (41, '41'),
        (42, '42'),
        (43, '43'),
        (45, '45'),
        (46, '46'),
        (47, '47'),
    ]

    size = models.IntegerField(choices=SIZE_CHOICES)
    shoe_id = models.ManyToManyField(Shoe)


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
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    # shoe_id = models.ManyToManyField(Shoe)

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

    # status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    comment = models.CharField(max_length=300, blank=True)

    # Utils
    date_created = models.DateField(default=timezone.now, auto_created=True, null=False)
    # date_delivered = models.DateField(default=None, auto_created=True, null=True)
    # delivered = models.DateField(default=False, null=False)

    def __str__(self):
        return "name: {}, comment: {}, order id: {}".format(self.user_id.name, self.comment, self.pk)

    def mark_delivered(self, commit=True):
        self.delivered = True
        self.date_delivered = timezone.now()
        if commit:
            self.save()
