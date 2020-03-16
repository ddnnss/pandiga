

from django.urls import path
from . import views

urlpatterns = [
    path('apply_code/', views.apply_code, name='apply_code'),





]
