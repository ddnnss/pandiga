import json
from .models import City
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

def create_city(request):
    from .sity_search import cities

    for i in cities:
        City.objects.create(city=i['city'],region=i['region'])
        print(i)

def get_city(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    print(request_body)
    cities = City.objects.filter(city__startswith=request_body['query'].capitalize())

    return_dict = list()
    for i in cities:
        return_dict.append({'id' : i.id, 'city': i.city, 'region': i.region})
    return JsonResponse(return_dict, safe=False)


def index(request):
    indexPage = True
    return render(request, 'staticPage/index.html', locals())


def login_page(request):
    if not request.user.is_authenticated:
        loginActive = 'menu-link-active '
        return render(request, 'staticPage/login.html', locals())
    else:
        return HttpResponseRedirect('/')

