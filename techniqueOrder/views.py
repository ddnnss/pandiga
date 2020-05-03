from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from technique.models import *
from .forms import *
from django.contrib import messages
import datetime
from technique.models import TechniqueType
from customuser.models import Notification

def technique_all_orders(request):
    if request.user.is_authenticated and not request.user.is_customer:
        all_orders = TechniqueOrder.objects.filter(is_active=True,
                                                   is_moderated=True,
                                                   worker__isnull=True).exclude(customer_id=request.user.id).order_by('-created_at')
        all_techique_types = TechniqueType.objects.all
        return render(request, 'techniqueOrder/all-technique-orders.html', locals())
    else:
        return HttpResponseRedirect('/')


def technique_order_detail(request,order_slug):
    if request.user.is_authenticated and not request.user.is_customer:
        order = get_object_or_404(TechniqueOrder, name_slug=order_slug)
        can_apply = False
        apply_accepted = False
        try:
            viewed = TechniqueOrderViewed.objects.get(order=order)
            viewed.users.add(request.user)
            viewed.save()
        except:
            viewed = TechniqueOrderViewed.objects.create(order=order)
            viewed.users.add(request.user)
            viewed.save()
        my_technique = TechniqueItem.objects.filter(owner=request.user).filter(sub_section=order.sub_section)
        try:
            my_applys = TechniqueOrderApply.objects.get(order=order, user=request.user)
        except:
            can_apply = True
            print('can_apply = True')
        if order.order_apply:
            order_apply = TechniqueOrderApply.objects.get(id=order.order_apply)
            if order_apply.user == request.user:
                apply_accepted = True
                print(' apply_accepted = True')

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
                tech = TechniqueItem.objects.filter(city=newOrder.city,sub_section=newOrder.sub_section)
                for t in tech:
                    if not t.owner.is_customer:
                        Notification.objects.create(user=t.owner,
                                                    text=f'Новая заявка на технику {newOrder.get_technique_name()}',
                                    is_chat_notification=False,
                                    redirect_url=f'/technique/orders/{newOrder.name_slug}')
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

def technique_order_apply(request):
    new_order = TechniqueOrderApply.objects.create(order_id=request.POST.get('order_id'),
                                       technique_id=request.POST.get('technique_for_order'),
                                       user_id=request.POST.get('user_id'),
                                       price=request.POST.get('price'))
    Notification.objects.create(user=new_order.order.customer,
                                text='Новый отклик на заявку',
                                is_chat_notification=False,
                                redirect_url=f'/user/lk/?tab=tab-my-order-detail&order_id={new_order.order.id}')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def technique_order_apply_decline(request,apply_id):
    apply = get_object_or_404(TechniqueOrderApply, id=apply_id)
    if apply.order.customer == request.user:
        apply.is_accepted = False
        apply.decline_date = datetime.datetime.now()
        apply.save()

    return HttpResponseRedirect(f'/user/lk/?tab=tab-my-order-detail&order_id={apply.order.id}')

def technique_order_apply_accept(request,apply_id):
    apply = get_object_or_404(TechniqueOrderApply, id=apply_id)
    if apply.order.customer == request.user:
        apply.is_accepted = True
        apply.accept_date = datetime.datetime.now()
        # ----------added----------------------
        apply.is_choosen = True
        apply.choose_date = datetime.datetime.now()
        apply.save()
        apply.order.worker = apply.user
        apply.order.order_apply = apply.id
        apply.order.save()

        for app in apply.order.applys.all():
            if app.id != apply.id:
                app.delete()
    # ----------added----------------------
        Notification.objects.create(user=apply.technique.owner,
                                    text='Ваше предложение на заявку принято',
                                    is_chat_notification=False,
                                    redirect_url=f'/technique/orders/{apply.order.name_slug}')
    return HttpResponseRedirect(f'/user/lk/?tab=tab-my-order-detail&order_id={apply.order.id}')


def order_apply_done(request, order_id):
    order = get_object_or_404(TechniqueOrder, id=order_id)
    if order.customer == request.user:
        order.is_finished = True
        order.save()
        Notification.objects.create(user=order.worker,
                                    text='Заявка успешно завершена',
                                    is_chat_notification=False,
                                    redirect_url=f'/technique/orders/{order.name_slug}')
    return HttpResponseRedirect(f'/user/lk/?tab=tab-my-order-detail&order_id={order.id}')

def technique_order_apply_decline_by_worker(request,apply_id):
    apply = get_object_or_404(TechniqueOrderApply, id=apply_id)
    if apply.user == request.user:
        apply.is_accepted = False
        apply.decline_date = datetime.datetime.now()
        apply.save()

    return HttpResponseRedirect('/user/lk/?tab=tab-my-orders-apply')

def technique_order_apply_accept_by_worker(request,apply_id):
    apply = get_object_or_404(TechniqueOrderApply, id=apply_id)
    if apply.user == request.user:
        apply.is_choosen = True
        apply.choose_date = datetime.datetime.now()
        apply.save()
        apply.order.worker=request.user
        apply.order.order_apply = apply.id
        apply.order.save()

        for app in apply.order.applys.all():
            if app.id != apply.id:
                app.delete()


    return HttpResponseRedirect('/user/lk/?tab=tab-my-orders-apply')