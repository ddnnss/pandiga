from django.shortcuts import render


def index(request):

    return render(request, 'staticPage/index.html', locals())