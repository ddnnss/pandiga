

from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.new, name='new_pay'),
    path('check/', views.check, name='check_pay'),




]
