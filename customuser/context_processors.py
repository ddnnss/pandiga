from technique.models import TechniqueItemFavorite,TechniqueItem
from chat.models import *
from techniqueOrder.models import *

import random
def check_profile(request):
    num1 = random.randint(0, 9)
    num2 = random.randint(0, 9)
    if request.user.is_authenticated:
        user = request.user
        profile_ok = False
        can_add_technique = True
        techniqueItemsFavorite = TechniqueItemFavorite.objects.filter(user=user)
        wishlist_ids = []
        for i in techniqueItemsFavorite:
            wishlist_ids.append(i.techniqueitem.id)
        my_technique = TechniqueItem.objects.filter(owner=user)
        my_technique_orders = TechniqueOrder.objects.filter(customer=user)
        my_tarif = user.tarif
        my_balance = user.balance
        if my_tarif.technique_count <= user.technique_added:
            can_add_technique = False
        can_call = my_tarif.can_call
        can_chat = my_tarif.can_chat



        if user.phone:
            profile_ok = True
        allChats = Chat.objects.filter(users__in=[user.id])
        all_orders_apply = TechniqueOrderApply.objects.filter(user=user,is_choosen=False)

        allUnreadChats = allChats.filter(isNewMessages=True).exclude(lastMsgBy=user)
        allReadChats = allChats.filter(isNewMessages=False)


    return locals()

