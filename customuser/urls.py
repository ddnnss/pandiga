from django.urls import path
from . import views

urlpatterns = [
   path('logout/', views.logout_page, name='logout_page'),
   path('send_sms/', views.send_sms, name='send_sms'),
   path('send_check_number/', views.send_check_number, name='send_check_number'),
   path('change_status/', views.change_status, name='change_status'),
   path('lk/', views.lk_page, name='lk_page'),
   path('update/', views.user_profile_update, name='user_profile_update'),
   path('user_phone/', views.user_phone, name='user_phone'),
]
