from django.http import HttpResponseRedirect
from django.shortcuts import render


def index(request):
    indexPage = True
    return render(request, 'staticPage/index.html', locals())


def login_page(request):
    if not request.user.is_authenticated:
        loginActive = 'menu-link-active '
        return render(request, 'staticPage/login.html', locals())
    else:
        return HttpResponseRedirect('/')

