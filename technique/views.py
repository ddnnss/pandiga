import json

from django.http import JsonResponse
from django.shortcuts import render
from .models import *


def technique_catalog(request):
    all_Technique = TechniqueType.objects.filter(is_active=True)
    catalogTechniqueActive = 'menu-link-active '
    return render(request, 'catalog/catalog.html', locals())

def add_technique(request):
    all_types = TechniqueType.objects.filter(is_active=True)
    addTechniqueActive = 'menu-link-active '
    return render(request, 'catalog/add-technique.html', locals())



def get_type_sublists(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    print(request_body)
    id = request_body['type']
    target = request_body['target']
    return_dict = list()

    if target == 'section':
        sections = TechniqueSection.objects.filter(type_id=id)
        for i in sections:
            return_dict.append({'id': i.id, 'name': i.name})
        return JsonResponse(return_dict, safe=False)
    if target == 'subsection':
        subsections = TechniqueSubSection.objects.filter(section_id=id)
        for i in subsections:
            return_dict.append({'id': i.id, 'name': i.name})
        return JsonResponse(return_dict, safe=False)



