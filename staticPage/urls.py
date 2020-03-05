

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login_page'),
    path('create_city/', views.create_city, name='create_city'),
    path('get_city/', views.get_city, name='get_city'),



]
