from django.contrib import admin
from started_app.models import *
from cart.models import *

# Register your models here.

admin.site.register(Shoe)
admin.site.register(Order)
admin.site.register(PaymentMethod)
admin.site.register(Material)
admin.site.register(Brand)
admin.site.register(Cart)

