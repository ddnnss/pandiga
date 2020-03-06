import json

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
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
    name_slug = request_body['type']
    target = request_body['target']
    return_dict = list()

    if target == 'section':
        sections = TechniqueSection.objects.filter(type__name_slug=name_slug)
        for i in sections:
            return_dict.append({'name_slug': i.name_slug, 'name': i.name})
        return JsonResponse(return_dict, safe=False)
    if target == 'subsection':
        subsections = TechniqueSubSection.objects.filter(section__name_slug=name_slug)
        for i in subsections:
            return_dict.append({'name_slug': i.name_slug, 'name': i.name})
        return JsonResponse(return_dict, safe=False)

def filter_qs(qs,filter_city=None,filter_section=None,filter_subsection=None,filter_search=None):
    result_qs = qs
    if filter_search:
        result_qs = result_qs.filter(name_lower__contains=filter_search.lower())
    if filter_city:
        result_qs = result_qs.filter(city_id=filter_city)
    if filter_section:
        result_qs = result_qs.filter(section__name_slug=filter_section)
    if filter_subsection:
        result_qs = result_qs.filter(sub_section__name_slug=filter_subsection)
    return result_qs
def technique_type_catalog(request, type_slug):
    current_technique_type = get_object_or_404(TechniqueType, name_slug=type_slug)
    all_technique_qs = TechniqueItem.objects.filter(type=current_technique_type, is_moderated=True, is_active=True)

    filter_city = request.GET.get('city') if request.GET.get('city') != 'all' else None
    #filter_type = request.GET.get('type') if request.GET.get('type') != 'all' else None
    filter_section = request.GET.get('section') if request.GET.get('section') != 'all' else None
    filter_subsection = request.GET.get('subsection') if request.GET.get('subsection') != 'all' else None
    filter_search = request.GET.get('search') if request.GET.get('search') != '' else None

    city_from_filter = City.objects.get(id=filter_city) if filter_city else ''
    section_from_filter = TechniqueSection.objects.get(name_slug=filter_section) if filter_section else ''
    subsection_from_filter = TechniqueSubSection.objects.get(name_slug=filter_subsection) if filter_subsection else ''

    if filter_city or filter_section or filter_subsection or filter_search:
        all_technique = filter_qs(all_technique_qs,filter_city,filter_section,filter_subsection, filter_search)
    else:
        all_technique = all_technique_qs
    return render(request, 'catalog/catalog_inner.html', locals())


def technique_section_catalog(request, type_slug, section_slug):
    current_technique_type = get_object_or_404(TechniqueType, name_slug=type_slug)
    current_technique_section = get_object_or_404(TechniqueSection, name_slug=section_slug)
    all_technique = TechniqueItem.objects.filter(section=current_technique_section, is_moderated=True, is_active=True)
    return render(request, 'catalog/catalog_inner.html', locals())

def technique_subsection_catalog(request, type_slug, section_slug, subsection_slug):
    current_technique_type = get_object_or_404(TechniqueType, name_slug=type_slug)
    current_technique_section = get_object_or_404(TechniqueSection, name_slug=section_slug)
    current_technique_subsection = get_object_or_404(TechniqueSubSection, name_slug=subsection_slug)
    all_technique = TechniqueItem.objects.filter(sub_section=current_technique_subsection, is_moderated=True, is_active=True)
    return render(request, 'catalog/catalog_inner.html', locals())