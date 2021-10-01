from django.contrib import admin
from django.urls import path, re_path
from . import views

app_name = 'started_app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('shoes/', views.ShowShoesView.as_view(), name='show_shoes'),
    path('shoes/<int:pk>', views.ShoeInfoView.as_view(), name='shoe_info'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('shoes/filter/', views.FilterView.as_view(), name='filter')
]
