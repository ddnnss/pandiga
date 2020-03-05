

from django.urls import path
from . import views

urlpatterns = [

    path('', views.technique_catalog, name='technique_catalog'),
    path('add-technique/', views.add_technique, name='add_technique'),
    path('get_type_sublists/', views.get_type_sublists, name='get_type_sublists'),
    path('<type_slug>/', views.technique_type_catalog, name='technique_type_catalog'),
    path('<type_slug>/<section_slug>/', views.technique_section_catalog, name='technique_section_catalog'),
    path('<type_slug>/<section_slug>/<subsection_slug>/', views.technique_subsection_catalog, name='technique_subsection_catalog'),


]
