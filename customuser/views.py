import json

from django.views.decorators.csrf import csrf_exempt

from .utils import create_random_string
from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404
from .forms import UpdateForm
from customuser.models import *
from django.http import JsonResponse, HttpResponseRedirect
from twilio.rest import Client
from chat.models import Chat
from ya_payment.models import *
from partner.models import *
from feedback.models import *
import uuid
from yandex_checkout import Configuration, Payment
import settings

from technique.models import *
from techniqueOrder.models import *

import datetime as dt
from datetime import datetime
from django.utils import timezone

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def send_sms(request):
    """Отправка смс кода подтверждения"""
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    print(request_body)
    request.session['user_phone'] = request_body['phone'].replace('(','').replace(')','').replace('-','')
    request.session['user_name'] = request_body['name']
    sms_number = create_random_string(digits=True)
    request.session['sms_number'] = sms_number

    print('sms_number=',sms_number)

    account_sid = settings.TWILLO_ACCOUNT_SID
    auth_token = settings.TWILLO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    messageSend = True
    try:
        message = client.messages.create(
            to=request.session['user_phone'],
            from_="test",
            body=f'PANDIGA. Код подтверждения: {sms_number}')
        print('message.sid=',message.sid)
        messageSend = True
    except:
        messageSend = False

    if messageSend:
        return JsonResponse({'result': 'send_ok', 'code': sms_number})
    else:
        return JsonResponse({'result': 'send_error'})


def send_check_number(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    phone = request.session['user_phone']
    name = request.session['user_name']
    print('request_body = ', request_body)
    if request_body['number'] == request.session['sms_number']:
        try:
            user = User.objects.get(phone=phone)
            print('User found')
            if user is not None:
                if user.is_active:
                    print('User found')
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return JsonResponse({'result': 'ok'})
                else:
                    return JsonResponse({'result': 'blocked'})
        except:
            user = User.objects.create(phone=phone,first_name=name)
            print(user.id)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return JsonResponse({'result': 'ok'})

    else:
        return JsonResponse({'result': 'number_error'})


def change_status(request):
    user = request.user
    if user.is_customer:
        user.is_customer = False
    else:
        user.is_customer = True
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def lk_page(request):
    user = request.user
    my_order_id = request.GET.get('order_id')
    lkPage=True
    all_tarif = Tarif.objects.all()
    all_payments_types = PaymentType.objects.all()
    all_payments = PaymentObj.objects.filter(user=user)
    all_partners = Parnter.objects.filter(code=user.partner_code)
    all_partners_money = PartnerMoney.objects.filter(partner__code=user.partner_code)
    all_notificatons = Notification.objects.filter(user=user, is_chat_notification=False).order_by('-createdAt')
    all_own_user_feedbacks = UserFeedback.objects.filter(from_user=user)
    all_own_tech_feedbacks = TechniqueFeedback.objects.filter(from_user=user)
    all_feedbacks_about_me = UserFeedback.objects.filter(about_user=user)
    all_feedbacks_about_my_tech = TechniqueFeedback.objects.filter(techniqueitem__owner=user)

    form = UpdateForm()
    if user.is_customer and  my_order_id:
        my_order = get_object_or_404(TechniqueOrder, id=my_order_id)
        if my_order.worker:
            apply = TechniqueOrderApply.objects.get(id=my_order.order_apply)
        elif my_order.is_finished:
            apply = TechniqueOrderApply.objects.get(id=my_order.order_apply)
        else:
            print('my_order.applys.all',my_order.applys.all)
            all_orders = my_order.applys.filter(is_choosen=False)
            order_apply = all_orders.filter(is_accepted__isnull=True)
            order_apply_accepted = all_orders.filter(is_accepted=True)
            order_apply_not_accepted = all_orders.filter(is_accepted=False)


    if not user.is_customer:
        in_progress = TechniqueOrder.objects.filter(worker=user,is_finished=False)
        all_orders = TechniqueOrderApply.objects.filter(user=user,is_choosen=False)
        order_apply = all_orders.filter(is_accepted__isnull=True)
        order_apply_accepted = all_orders.filter(is_accepted=True)
        order_apply_not_accepted = all_orders.filter(is_accepted=False)

    return render(request, 'user/lk.html', locals())

def user_profile_update(request):
    print(request.POST)
    form = UpdateForm(request.POST, request.FILES, instance=request.user)
    print(form.errors)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/user/lk/?tab=tab-profile')
    else:
        form = UpdateForm()
    return HttpResponseRedirect("/user/lk/?tab=tab-profile")


def user_phone(request):
    if request.user.tarif.can_see_phone:
        request_unicode = request.body.decode('utf-8')
        request_body = json.loads(request_unicode)
        user_id = request_body['iid']
        user = get_object_or_404(User, id=user_id)
        return JsonResponse({'phone': user.phone})
    else:
        return JsonResponse({'status': 'error'}, safe=False)

def mark_notify_read(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    user_id = request_body['id']
    all_notify = Notification.objects.filter(user_id=user_id)
    for notify in all_notify:
        notify.is_read = True
        notify.save()
    return JsonResponse({'result': 'ok'})


def get_notifications(request):
    response_dict={}
    notifications=[]
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    user_id = request_body['id']
    user = User.objects.get(id=user_id)
    allChats = Chat.objects.filter(users__in=[user_id])
    all_notify = Notification.objects.filter(user=user, is_read=False)
    for n in all_notify:
        if n.is_delayed and timezone.now()  > n.show_time:
            print('can see')
            n.is_delayed=False
            n.save()
        else:
            print('NOT SEE')
    all_notify_not_notified = all_notify.filter(is_user_notified=False, is_delayed=False)
    for notify in all_notify_not_notified:
        notify.is_user_notified = True
        notify.save()
        notifications.append({
           'text':notify.text,
            'url':notify.redirect_url
        })
    response_dict['notify'] = notifications
    response_dict['notifications_count'] = all_notify.filter(is_chat_notification=False, is_delayed=False).count()
    response_dict['unread_chat_count'] = allChats.filter(isNewMessages=True).exclude(lastMsgBy_id=user_id).count()
    return JsonResponse(response_dict)

def del_notifications(request,n_id):
    notify = get_object_or_404(Notification, id=n_id)
    if notify.user == request.user:
        notify.delete()
    return HttpResponseRedirect("/user/lk/?tab=tab-notification")

def user_profile(request,user_id):
    current_user = get_object_or_404(User, id=user_id)
    return render(request, 'user/public-profile.html', locals())
