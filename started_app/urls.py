from django.contrib import admin
from django.urls import path, re_path
from started_app import views
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('users/', views.ShowUsersView.as_view(), name='show-users'),
    path('<int:pk>/', views.UserInfoView.as_view(), name='user-info'),
    path('<int:pk>/add_order/', views.OrderCreate.as_view(), name='add_order'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('shoes/', views.ShowShoesView.as_view(), name='show_shoes'),
    path('shoes/<int:pk>', views.ShoeInfoView.as_view(), name='shoe_info'),
    path('<int:pk>/thanks/', views.ThanksView.as_view(), name='thanks'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<int:shoe_id>', views.AddToCartView.as_view(), name='add_to_cart'),
    path('del-from-cart/<int:shoe_id>', views.DelFromCartView.as_view(), name='del_from_cart'),
]
