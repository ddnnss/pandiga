import json

from django.contrib.auth import authenticate, login, logout
from customuser.models import *
from django.http import JsonResponse, HttpResponseRedirect
from twilio.rest import Client
import settings

def create_random_string(digits=False, num=4):
    from random import choices
    import string
    if digits:
        random_string = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=num))
    else:
        random_string = ''.join(choices(string.digits, k=num))
    return random_string

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def phone_login(request):
    pass


def send_sms(request):
    """Отправка смс кода подтверждения"""
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    print(request_body)
    request.session['user_phone'] = request_body['phone'].replace('(','').replace(')','').replace('-','')
    request.session['user_name'] = request_body['name']
    sms_number = create_random_string()
    request.session['sms_number'] = sms_number

    print('sms_number=',sms_number)

    account_sid = settings.TWILLO_ACCOUNT_SID
    auth_token = settings.TWILLO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    messageSend = True
    # try:
    #     message = client.messages.create(
    #         to=request.session['user_phone'],
    #         from_="test",
    #         body=f'PANDIGA. Код подтверждения: {sms_number}')
    #     print('message.sid=',message.sid)
    #     messageSend = True
    # except:
    #     messageSend = False

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






def log_in(request):
    return_dict = {}
    phone = request.POST.get('phone')
    password = request.POST.get('password')
    print(phone)
    user = authenticate(phone=phone, password=password)
    print(user)
    if user is not None:
        if user.is_active:
            login(request, user)
            return_dict['result'] = 'ok'
            return JsonResponse(return_dict)
        else:
            return_dict['result'] = 'inactive'
            return JsonResponse(return_dict)
    else:
        return_dict['result'] = 'invalid'
        return JsonResponse(return_dict)



