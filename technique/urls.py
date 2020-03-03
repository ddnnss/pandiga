

from django.urls import path
from . import views

urlpatterns = [
    path('', views.technique_catalog, name='technique_catalog'),
    path('add-technique/', views.add_technique, name='add_technique'),
    path('get_type_sublists/', views.get_type_sublists, name='get_type_sublists'),


]
