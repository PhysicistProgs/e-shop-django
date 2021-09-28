from django.urls import path, re_path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('/add/<int:shoe_id>', views.AddToCartView.as_view(), name='add'),
    path('/remove/<int:shoe_id>', views.DelFromCartView.as_view(), name='remove'),
]
