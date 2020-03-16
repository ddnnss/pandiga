from django.http import HttpResponseRedirect
from django.shortcuts import render
import uuid
from yandex_checkout import Configuration, Payment
from .models import *
import settings
from partner.models import *

def new(request):
    amount = request.POST.get('amount')
    payment_type = request.POST.get('payment_type')

    Configuration.account_id = settings.YA_SHOP_ID
    Configuration.secret_key = settings.YA_API

    payment = Payment.create({
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "payment_method": {
            "type": payment_type,
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f'{settings.HOST}/pay/check'
        },
        "capture": True,
        "description": f'Пополнение баланса пользователя ID {request.user.id}. {request.user.get_full_name()}'
    }, uuid.uuid4())

    pt = PaymentType.objects.get(method=payment_type)
    PaymentObj.objects.create(user=request.user,
                           pay_id=payment.id,
                           amount=int(amount),
                           type=pt,
                           status='Не оплачен')

    return HttpResponseRedirect(payment.confirmation.confirmation_url)

def check(request):
    Configuration.account_id = settings.YA_SHOP_ID
    Configuration.secret_key = settings.YA_API

    all_payments = PaymentObj.objects.filter(user=request.user, is_payed=False)

    for pay in all_payments:
        payment = Payment.find_one(pay.pay_id)
        if payment.status == 'succeeded':
            pay.is_payed = True
            pay.status = 'Оплачен'
            pay.save()
            request.user.balance += pay.amount
            request.user.save()

            all_partners = Parnter.objects.filter(user=request.user)

            if all_partners.exists():
                for partner in all_partners:
                    partner_user = User.objects.get(partner_code=partner.code)
                    partner_user_parnter_bonus = partner_user.tarif.parter_bonus
                    earned = int(pay.amount * partner_user_parnter_bonus / 100)
                    partner_user.partner_balance += earned
                    partner_user.save()
                    partner.total_earned += earned
                    partner.save()
                    PartnerMoney.objects.create(partner=partner,
                                                earned=earned,
                                                action='Пополнение баланса')

    return HttpResponseRedirect('/user/lk/?tab=tab-finance')
