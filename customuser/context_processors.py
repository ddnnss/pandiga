from technique.models import TechniqueItemFavorite,TechniqueItem
from chat.models import *

import random
def check_profile(request):
    num1 = random.randint(0, 9)
    num2 = random.randint(0, 9)
    if request.user.is_authenticated:
        techniqueItemsFavorite = TechniqueItemFavorite.objects.filter(user=request.user)
        ownTecnique = TechniqueItem.objects.filter(owner=request.user)

        allChats = Chat.objects.filter(users__in=[request.user.id])


        allUnreadChats = allChats.filter(isNewMessages=True)
        allReadChats = allChats.filter(isNewMessages=False)


    return locals()

