from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from customuser.models import *
from django.http import JsonResponse, HttpResponseRedirect
# from .forms import SignUpForm , UpdateForm

from django.core.mail import send_mail
from django.template.loader import render_to_string



def create_password():
    from random import choices
    import string
    password = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
    return password

def vk_login(request):
    pass

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



