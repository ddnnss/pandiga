from django.shortcuts import render


def index(request):
    indexPage = True
    return render(request, 'staticPage/index.html', locals())


def login_page(request):
    try:
        print(request.session['phone_for_verify'])
    except:
        pass
    return render(request, 'staticPage/login.html', locals())


