

from django.urls import path
from . import views

urlpatterns = [
    path('new_msg/', views.new_msg, name='new_msg'),
    path('to_rent/', views.to_rent, name='to_rent'),
    path('get_chats/', views.get_chats, name='get_chats'),
    path('get_msg/', views.get_msg, name='get_msg'),
    path('add_msg/', views.add_msg, name='add_msg'),
    path('delete_chat/', views.delete_chat, name='delete_chat'),



]
