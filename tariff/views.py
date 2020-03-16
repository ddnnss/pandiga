from django.http import HttpResponseRedirect
from .models import Tarif
from datetime import datetime
from dateutil.relativedelta import relativedelta

def change_tarif(request,id):
    user = request.user
    tarif = Tarif.objects.get(id=id)
    user.tarif = tarif
    user.tariff_update = datetime.today()
    user.tariff_expire = datetime.today() + relativedelta(months=1)
    user.balance -= tarif.price
    user.save()
    return HttpResponseRedirect('/user/lk/?tab=tab-tarif')
