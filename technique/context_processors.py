from .models import *


def get_technique(request):
    all_technique_types = TechniqueType.objects.all()
    rating = range(1,6)
    return locals()

