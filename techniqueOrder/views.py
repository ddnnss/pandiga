from django.http import HttpResponseRedirect
from django.shortcuts import render
from technique.models import *
from .forms import *
from django.contrib import messages

def technique_order(request):
    if request.POST:
        print(request.POST)
        newOrder = None
        form = TechniqueOrderForm(request.POST)
        if form.is_valid():
            newOrder = form.save(commit=False)
            newOrder.customer = request.user
            newOrder.save()
            print(newOrder.id)
            messages.success(request, 'Спасибо, форма успешно отправлена')
        else:
            print(form.errors)
            messages.error(request, 'Все поля обязвтельны для заполнения')

        return HttpResponseRedirect('/technique/order/')
    all_types = TechniqueType.objects.filter(is_active=True)
    form = TechniqueOrderForm()
    addTechniqueOrderActive = 'menu-link-active '
    return render(request, 'catalog/technique-order.html', locals())
