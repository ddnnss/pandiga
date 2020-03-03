from django.urls import path
from . import views

urlpatterns = [
   path('logout/', views.logout_page, name='logout_page'),
   path('phone_login/', views.phone_login, name='phone_login'),
   path('send_sms/', views.send_sms, name='send_sms'),
   path('send_check_number/', views.send_check_number, name='send_check_number'),
]
