from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login_page'),
    path('about/', views.about, name='about'),
    path('for-partners/', views.forpartners, name='forpartners'),
    path('servicerules/', views.servicerules, name='servicerules'),
    path('licenzionnoe-soglashenie/', views.licenzionnoe_soglashenie, name='licenzionnoe_soglashenie'),
    path('privacy-policy/', views.privacypolicy, name='privacypolicy'),
    path('publichnyj-agentskij-dogovor/', views.publichnyj_agentskij_dogovor, name='publichnyj_agentskij_dogovor'),
    path('usloviya-ispolzovaniya/', views.usloviya_ispolzovaniya, name='usloviya_ispolzovaniya'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('servicerules/', views.servicerules, name='servicerules'),
    path('for-technique-owners/', views.fortechniqueowners, name='fortechniqueowners'),
    path('tariff/', views.tariff, name='tariff'),
    path('questions/', views.questions, name='questions'),
    path('contacts/', views.contacts, name='contacts'),
    # path('create_city/', views.create_city, name='create_city'),
    # path('type/', views.type, name='create_city'),
    # path('section/', views.section, name='create_city'),
    # path('subsection/', views.subsection, name='create_city'),
    # path('item/', views.tech, name='create_city'),
    # path('user/', views.user, name='create_city'),
    path('get_city/', views.get_city, name='get_city'),
    path('index.html', RedirectView.as_view(url='/', permanent=False), name='index1'),
    path('index.php', RedirectView.as_view(url='/', permanent=False), name='index2'),
    path('robots.txt', views.robots, name='robots'),


]
