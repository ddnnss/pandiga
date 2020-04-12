from django.http import HttpResponseRedirect
from .models import Tarif
from datetime import datetime
from dateutil.relativedelta import relativedelta
from customuser.models import Notification

def change_tarif(request,id):
    user = request.user
    tarif = Tarif.objects.get(id=id)
    user.tarif = tarif
    user.tariff_update = datetime.today()
    user.tariff_expire = datetime.today() + relativedelta(months=1)
    user.balance -= tarif.price
    user.save()
    Notification.objects.create(user=user,
                               text='Тариф был успешно изменен')
    return HttpResponseRedirect('/user/lk/?tab=tab-tarif')
