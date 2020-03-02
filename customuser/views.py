from django.contrib.auth import authenticate, login, logout
from customuser.models import *
from django.http import JsonResponse, HttpResponseRedirect


def create_random_string(digits=False, num=4):
    from random import choices
    import string
    if digits:
        random_string = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=num))
    else:
        random_string = ''.join(choices(string.digits, k=num))
    return random_string

def vk_login(request):
    pass


def phone_login(request):
    pass


def send_sms(request):
    request.session['user_phone'] = 'blueq'
    request.session['user_name'] = 'blueq'

    return JsonResponse({'foo': 'bar'})



def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')


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



