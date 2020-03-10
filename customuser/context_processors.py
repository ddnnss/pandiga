from technique.models import TechniqueItemFavorite,TechniqueItem
from chat.models import *
from techniqueOrder.models import *

import random
def check_profile(request):
    num1 = random.randint(0, 9)
    num2 = random.randint(0, 9)
    if request.user.is_authenticated:
        user = request.user
        techniqueItemsFavorite = TechniqueItemFavorite.objects.filter(user=user)
        wishlist_ids = []
        for i in techniqueItemsFavorite:
            wishlist_ids.append(i.techniqueitem.id)
        my_technique = TechniqueItem.objects.filter(owner=user)
        my_technique_orders = TechniqueOrder.objects.filter(customer=user)

        allChats = Chat.objects.filter(users__in=[user.id])


        allUnreadChats = allChats.filter(isNewMessages=True)
        allReadChats = allChats.filter(isNewMessages=False)


    return locals()

