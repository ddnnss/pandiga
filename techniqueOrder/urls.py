

from django.urls import path
from . import views

urlpatterns = [


    path('new-order/', views.technique_order, name='technique_order'),
    path('decline-apply/<apply_id>', views.technique_order_apply_decline, name='technique_order_apply_decline'),
    path('decline-apply-w/<apply_id>', views.technique_order_apply_decline_by_worker, name='technique_order_apply_decline_by_worker'),
    path('accept-apply/<apply_id>', views.technique_order_apply_accept, name='technique_order_apply_accept'),
    path('order-apply-done/<order_id>', views.order_apply_done, name='order_apply_done'),
    path('accept-apply-w/<apply_id>', views.technique_order_apply_accept_by_worker, name='technique_order_apply_accept_by_worker'),
    path('new-order-apply/', views.technique_order_apply, name='technique_order_apply'),
    path('orders/', views.technique_all_orders, name='technique_all_orders'),
    path('orders/<order_slug>', views.technique_order_detail, name='technique_order_detail'),




]
