

from django.urls import path
from . import views

urlpatterns = [
    path('change/<id>', views.change_tarif, name='change_tarif'),





]
