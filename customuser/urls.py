from django.urls import path
from . import views

urlpatterns = [
   path('vk_login/', views.vk_login, name='vk_login'),
   path('phone_login/', views.phone_login, name='phone_login'),
   path('send_sms/', views.send_sms, name='send_sms'),
]
