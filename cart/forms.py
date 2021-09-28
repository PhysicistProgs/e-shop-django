from cart.models import CartProducts
from django.forms import ModelForm


class ShoeQuantityForm(ModelForm):
    class Meta:
        model = CartProducts
        fields = ['quantity']