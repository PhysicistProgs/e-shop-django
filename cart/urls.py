from django.urls import path, re_path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('/add/<int:shoe_id>', views.AddToCartView.as_view(), name='add'),
    path('/remove/<int:shoe_id>', views.DelFromCartView.as_view(), name='remove'),
    path('<int:pk>/order/', views.OrderView.as_view(), name='order'),
    path('create_order/', views.OrderCreate.as_view(), name='create_order'),
]
