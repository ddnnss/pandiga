from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from customuser.models import User


def apply_code(request):
    partner_code = request.POST.get('partner_code')
    user_promo = None
    try:
        user_promo = User.objects.get(partner_code= partner_code)
        print('User found')
    except:
        user_promo = None
    if user_promo and user_promo != request.user:
        print('User is ok')
        try:
            Parnter.objects.get(code=partner_code, user=request.user)
            print('Partner user is present')
        except:
            Parnter.objects.create(code=partner_code, user=request.user)
            print('Partner user is NOT present')

    return HttpResponseRedirect('/user/lk/?tab=tab-money-earn')






