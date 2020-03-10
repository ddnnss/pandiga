

from django.urls import path
from . import views

urlpatterns = [


    path('new-order/', views.technique_order, name='technique_order'),
    path('orders/', views.technique_all_orders, name='technique_all_orders'),
    path('orders/<order_slug>', views.technique_order_detail, name='technique_order_detail'),



]
