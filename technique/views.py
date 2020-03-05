import json

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib import messages

def technique_catalog(request):
    all_Technique = TechniqueType.objects.filter(is_active=True)
    catalogTechniqueActive = 'menu-link-active '
    return render(request, 'catalog/catalog.html', locals())

def add_technique(request):
    if request.POST:
        newItem = None
        form = AddTechniqueForm(request.POST)
        if form.is_valid():
            newItem = form.save(commit=False)
            newItem.owner = request.user
            newItem.save()
            print(newItem.id)
            messages.success(request, 'Спасибо, форма успешно отправлена')
        else:
            print(form.errors)
            messages.error(request, 'Все поля обязвтельны для заполнения')
        if newItem:
            for f in request.FILES.getlist('item_images'):
                TechniqueItemImage.objects.create(techniqueitem_id=newItem.id, image=f).save()

            for f in request.FILES.getlist('item_docs'):
                TechniqueItemDoc.objects.create(techniqueitem_id=newItem.id, image=f).save()

        return HttpResponseRedirect('/catalog/add-technique/')
    #----POST-------
    all_types = TechniqueType.objects.filter(is_active=True)
    form = AddTechniqueForm()
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



