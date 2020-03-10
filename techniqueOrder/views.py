from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from technique.models import *
from .forms import *
from django.contrib import messages


def technique_all_orders(request):
    if request.user.is_authenticated and not request.user.is_customer:
        all_orders = TechniqueOrder.objects.filter(is_active=True,is_moderated=True)
        return render(request, 'techniqueOrder/all-technique-orders.html', locals())
    else:
        return HttpResponseRedirect('/')


def technique_order_detail(request,order_slug):
    if request.user.is_authenticated and not request.user.is_customer:
        order = get_object_or_404(TechniqueOrder, name_slug=order_slug)
        my_technique = TechniqueItem.objects.filter(owner=request.user).filter(sub_section=order.sub_section)
        print(my_technique)
        return render(request, 'techniqueOrder/technique-order-detail.html', locals())
    else:
        return HttpResponseRedirect('/')

def technique_order(request):
    if request.user.is_authenticated and request.user.is_customer:
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

            return HttpResponseRedirect('/technique/new-order/')
        all_types = TechniqueType.objects.filter(is_active=True)
        form = TechniqueOrderForm()
        addTechniqueOrderActive = 'menu-link-active '
        return render(request, 'techniqueOrder/technique-order.html', locals())
    else:
        return HttpResponseRedirect('/')
