

from django.urls import path
from . import views

urlpatterns = [


    path('order/', views.technique_order, name='technique_order'),



]
