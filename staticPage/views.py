import json
from .models import City
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from tariff.models import Tarif
from technique.models import TechniqueItem
import settings
#----
# from openpyxl import load_workbook
# from customuser.models import *
# from technique.models import *

#


def get_city(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    print(request_body)
    cities = City.objects.filter(city__startswith=request_body['query'].capitalize())

    return_dict = list()
    for i in cities:
        return_dict.append({'id' : i.id, 'city': i.city, 'region': i.region, 'coefficient': i.coefficient})
    return JsonResponse(return_dict, safe=False)


def index(request):
    indexPage = True
    page_title = 'PANDIGA - Клубная аренда техники'
    page_description = ''

    all_technique = TechniqueItem.objects.random(8)
    return render(request, 'staticPage/index.html', locals())


def login_page(request):
    if not request.user.is_authenticated:
        loginActive = 'menu-link-active '
        return render(request, 'staticPage/login.html', locals())
    else:
        return HttpResponseRedirect('/')

def robots(request):
    subdomain = request.subdomain
    if subdomain and not request.homedomain:
        robotsTxt = f"User-agent: *\nDisallow: /admin/\nUser-Agent: Googlebot\nDisallow: /\nHost: {settings.PROTOCOL}{subdomain.name}.{settings.MAIN_DOMAIN}.ru/\nSitemap:{settings.PROTOCOL}{subdomain.name}.{settings.MAIN_DOMAIN}.ru/sitemap.xml"
    else:
        robotsTxt = f"User-agent: *\nDisallow: /admin/\nHost: {settings.PROTOCOL}{settings.MAIN_DOMAIN}.ru/\nSitemap: {settings.PROTOCOL}{settings.MAIN_DOMAIN}.ru/sitemap.xml"

    return HttpResponse(robotsTxt, content_type="text/plain")

def about(request):
    return render(request, 'staticPage/about.html', locals())
def forpartners(request):
    return render(request, 'staticPage/forpartners.html', locals())
def servicerules(request):
    return render(request, 'staticPage/servicerules.html', locals())
def fortechniqueowners(request):
    return render(request, 'staticPage/forperformers.html', locals())
def tariff(request):
    return render(request, 'staticPage/tariff.html', locals())
def questions(request):
    return render(request, 'staticPage/questions.html', locals())
def contacts(request):
    return render(request, 'staticPage/contacts.html', locals())
def tarif(request):
    all_tarif = Tarif.objects.all()
    return render(request, 'staticPage/tarif_page.html', locals())
def licenzionnoe_soglashenie(request):
    return render(request, 'staticPage/servicerules-licenzionnoe_soglashenie.html', locals())

def privacypolicy(request):
    return render(request, 'staticPage/servicerules-privacypolicy.html', locals())

def publichnyj_agentskij_dogovor(request):
    return render(request, 'staticPage/servicerules-publichnyj_agentskij_dogovor.html', locals())
def usloviya_ispolzovaniya(request):
    return render(request, 'staticPage/servicerules-usloviya_ispolzovaniya.html', locals())
def vacancies(request):
    return render(request, 'staticPage/vacancies.html', locals())