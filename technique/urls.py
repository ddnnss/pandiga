

from django.urls import path
from . import views

urlpatterns = [

    path('', views.technique_catalog, name='technique_catalog'),
    path('add-technique/', views.add_technique, name='add_technique'),
    path('del-technique/<id>', views.del_technique, name='del_technique'),
    path('edit-technique/<id>', views.edit_technique, name='edit_technique'),
    path('updateTechnique/', views.updateTechnique, name='updateTechnique'),
    path('change_technique_status/<id>', views.change_technique_status, name='change_technique_status'),
    path('add-to-favorite/<item_id>', views.add_to_favorite, name='add_to_favorite'),
    path('del_from_favorite/<item_id>', views.del_from_favorite, name='del_from_favorite'),
    path('get_type_sublists/', views.get_type_sublists, name='get_type_sublists'),
    path('<type_slug>/', views.technique_type_catalog, name='technique_type_catalog'),
    path('<type_slug>/<section_slug>/', views.technique_section_catalog, name='technique_section_catalog'),
    path('<type_slug>/<section_slug>/<subsection_slug>/', views.technique_subsection_catalog, name='technique_subsection_catalog'),
    path('<type_slug>/<section_slug>/<subsection_slug>/<technique_slug>', views.technique, name='technique'),
    path('section_subscribe', views.section_subscribe, name='section_subscribe'),


]
