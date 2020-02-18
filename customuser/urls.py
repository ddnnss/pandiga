from django.urls import path
from . import views

urlpatterns = [
   path('vk_login/', views.vk_login, name='vk_login'),

]
