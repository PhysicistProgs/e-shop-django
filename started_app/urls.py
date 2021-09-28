from django.contrib import admin
from django.urls import path, re_path
from . import views

app_name = 'started_app'

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
]
