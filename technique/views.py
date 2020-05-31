import json
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from feedback.models import TechniqueFeedback
from staticPage.models import *

def technique_catalog(request):

    catalogTechniqueActive = 'menu-link-active '
    return render(request, 'catalog/catalog.html', locals())

def add_to_favorite(request,item_id):
    techniqueItem = get_object_or_404(TechniqueItem, id=item_id)
    TechniqueItemFavorite.objects.create(user=request.user,techniqueitem=techniqueItem)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def del_from_favorite(request,item_id):
    techniqueItem = get_object_or_404(TechniqueItem, id=item_id)
    item = TechniqueItemFavorite.objects.get(user=request.user,techniqueitem=techniqueItem)
    item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def del_technique(request,id):
    techniqueItem = get_object_or_404(TechniqueItem, id=id)
    if techniqueItem.owner == request.user:
        request.user.technique_added -= 1
        request.user.save()
        techniqueItem.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def edit_technique(request,id):
    techniqueItem = get_object_or_404(TechniqueItem, id=id)
    if techniqueItem.owner == request.user:
        form = EditTechniqueForm()
        all_types = TechniqueType.objects.filter(is_active=True)
        return render(request, 'catalog/edit-technique.html', locals())
    else:
        return HttpResponseRedirect('/')

def updateTechnique(request):
    new_image = 0
    item = TechniqueItem.objects.get(id=request.POST.get('item_id'))
    for f in request.FILES.getlist('item_images'):
        print(f)
    form = EditTechniqueForm(request.POST, request.FILES, instance=item)
    if form.is_valid():
        new_image = form.save()
        print(new_image.id)
    else:
        print(form.errors)
    if request.FILES.getlist('item_images'):
        print('have images')
        all_images = item.images.all()
        all_images.delete()
        for f in request.FILES.getlist('item_images'):
            TechniqueItemImage.objects.create(techniqueitem=item, image=f)
    return HttpResponseRedirect('/user/lk/?tab=tab-my-cars')

def change_technique_status(request,id):
    techniqueItem = get_object_or_404(TechniqueItem, id=id)
    if techniqueItem.owner == request.user:
        if techniqueItem.is_free:
            techniqueItem.is_free = False
        else:
            techniqueItem.is_free = True
        techniqueItem.save()
        return HttpResponseRedirect('/user/lk/?tab=tab-my-cars')

def add_technique(request):
    if request.POST:
        newItem = None
        sub_section = TechniqueSubSection.objects.get(id=request.POST.get('sub_section'))
        city = City.objects.get(id=request.POST.get('city'))
        price = round(sub_section.section.base_price * city.coefficient)
        print(price)
        form = AddTechniqueForm(request.POST)
        if form.is_valid() and request.user.balance >= price:
            newItem = form.save(commit=False)
            newItem.owner = request.user
            newItem.save()
            request.user.technique_added += 1
            request.user.balance -= price
            request.user.save()
            print(newItem.id)
            TechniqueItemHistory.objects.create(techniqueitem=newItem,user=request.user,summ=price)
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
            return_dict.append({'name_slug': i.name_slug, 'name': i.name,'price':i.base_price})
        return JsonResponse(return_dict, safe=False)
    if target == 'subsection':
        subsections = TechniqueSubSection.objects.filter(section__name_slug=name_slug)
        for i in subsections:
            return_dict.append({'id':i.id, 'name_slug': i.name_slug, 'name': i.name})
        return JsonResponse(return_dict, safe=False)


def filter_qs(qs,filter_city=None,
              filter_section=None,
              filter_subsection=None,
              filter_search=None,
              filter_time_type=None,
              filter_h_from=None,
              filter_h_to=None,
              filter_h_price_from=None,
              filter_h_price_to=None,
              filter_d_from=None,
              filter_d_to=None,
              filter_d_price_from=None,
              filter_d_price_to=None
              ):
    print('filter_time_type', filter_time_type)
    result_qs = qs
    if filter_search:
        result_qs = result_qs.filter(name_lower__contains=filter_search.lower())
    if filter_city:
        result_qs = result_qs.filter(city_id=filter_city)
    if filter_section:
        result_qs = result_qs.filter(section__name_slug=filter_section)
    if filter_subsection:
        result_qs = result_qs.filter(sub_section__name_slug=filter_subsection)
    if filter_h_from and filter_h_to:
        result_qs = result_qs.filter(rent_type='hour')
        result_qs = result_qs.filter(Q(min_rent_time__lte=filter_h_to) & Q(min_rent_time__gte=filter_h_from))
        result_qs = result_qs.filter(Q(rent_price__lte=filter_h_price_to) & Q(rent_price__gte=filter_h_price_from))
    if filter_d_from and filter_d_to:
        result_qs = result_qs.filter(rent_type='day')
        result_qs = result_qs.filter(Q(min_rent_time__lte=filter_d_to) & Q(min_rent_time__gte=filter_d_from))
        result_qs = result_qs.filter(Q(rent_price__lte=filter_d_price_to) & Q(rent_price__gte=filter_d_price_from))

    return result_qs


def technique_type_catalog(request, type_slug):
    current_technique_type = get_object_or_404(TechniqueType, name_slug=type_slug)

    seo_text, page_h1, page_title, page_description = current_technique_type.get_seo_text(request=request)

    all_technique_qs = TechniqueItem.objects.filter(type=current_technique_type, is_moderated=True, is_active=True)
    if not request.user.is_authenticated:
        filter_city = request.GET.get('city') if request.GET.get('city') != 'all' else None
    else:
        print('filter_city for auth=', request.user.city.id)
        filter_city = request.GET.get('city') if request.GET.get('city') != 'all' else None
        if not filter_city:
            filter_city = request.user.city.id
    print('filter_city=',filter_city)
    #filter_type = request.GET.get('type') if request.GET.get('type') != 'all' else None
    filter_section = request.GET.get('section') if request.GET.get('section') != 'all' else None
    filter_subsection = request.GET.get('subsection') if request.GET.get('subsection') != 'all' else None
    filter_search = request.GET.get('search') if request.GET.get('search') != '' else None

    filter_time_type = request.GET.get('time_type') if request.GET.get('time_type') != '' else None

    filter_h_from = request.GET.get('h_from') if request.GET.get('h_from') != '' else None
    filter_h_to = request.GET.get('h_to') if request.GET.get('h_to') != '' else None
    filter_h_price_from = request.GET.get('h_price_from') if request.GET.get('h_price_from') != '' else None
    filter_h_price_to = request.GET.get('h_price_to') if request.GET.get('h_price_to') != '' else None

    filter_d_from = request.GET.get('d_from') if request.GET.get('d_from') != '' else None
    filter_d_to = request.GET.get('d_to') if request.GET.get('d_to') != '' else None
    filter_d_price_from = request.GET.get('d_price_from') if request.GET.get('d_price_from') != '' else None
    filter_d_price_to = request.GET.get('d_price_to') if request.GET.get('d_price_to') != '' else None


    city_from_filter = City.objects.get(id=filter_city) if filter_city else ''
    section_from_filter = TechniqueSection.objects.get(name_slug=filter_section) if filter_section else ''
    subsection_from_filter = TechniqueSubSection.objects.get(name_slug=filter_subsection) if filter_subsection else ''

    if filter_city or filter_section or filter_subsection or filter_search or filter_h_from or filter_d_from:
        all_technique = filter_qs(all_technique_qs,
                                  filter_city,
                                  filter_section,
                                  filter_subsection,
                                  filter_search,
                                  filter_time_type,
                                  filter_h_from,
                                  filter_h_to,
                                  filter_h_price_from,
                                  filter_h_price_to,
                                  filter_d_from,
                                  filter_d_to,
                                  filter_d_price_from,
                                  filter_d_price_to
                                  )
    else:
        all_technique = all_technique_qs
    return render(request, 'catalog/catalog_inner.html', locals())


def technique_section_catalog(request, type_slug, section_slug):
    print('\sectiopn')
    current_technique_type = get_object_or_404(TechniqueType, name_slug=type_slug)
    current_technique_section = get_object_or_404(TechniqueSection, name_slug=section_slug)
    is_subscribed = False
    seo_text, page_h1, page_title, page_description = current_technique_section.get_seo_text(request=request)
    print(seo_text, page_h1, page_title, page_description)
    all_technique_qs = TechniqueItem.objects.filter(section=current_technique_section, is_moderated=True, is_active=True)
    # filter_city = request.GET.get('city') if request.GET.get('city') != 'all' else None
    if not request.user.is_authenticated:
        filter_city = request.GET.get('city') if request.GET.get('city') != 'all' else None
    else:
        print('filter_city for auth=', request.user.city.id)
        filter_city = request.GET.get('city') if request.GET.get('city') != 'all' else None
        if not filter_city:
            filter_city = request.user.city.id
    print('filter_city=', filter_city)
    # filter_type = request.GET.get('type') if request.GET.get('type') != 'all' else None
    filter_section = request.GET.get('section') if request.GET.get('section') != 'all' else None
    filter_subsection = request.GET.get('subsection') if request.GET.get('subsection') != 'all' else None
    filter_search = request.GET.get('search') if request.GET.get('search') != '' else None

    filter_time_type = request.GET.get('time_type') if request.GET.get('time_type') != '' else None

    filter_h_from = request.GET.get('h_from') if request.GET.get('h_from') != '' else None
    filter_h_to = request.GET.get('h_to') if request.GET.get('h_to') != '' else None
    filter_h_price_from = request.GET.get('h_price_from') if request.GET.get('h_price_from') != '' else None
    filter_h_price_to = request.GET.get('h_price_to') if request.GET.get('h_price_to') != '' else None

    filter_d_from = request.GET.get('d_from') if request.GET.get('d_from') != '' else None
    filter_d_to = request.GET.get('d_to') if request.GET.get('d_to') != '' else None
    filter_d_price_from = request.GET.get('d_price_from') if request.GET.get('d_price_from') != '' else None
    filter_d_price_to = request.GET.get('d_price_to') if request.GET.get('d_price_to') != '' else None

    city_from_filter = City.objects.get(id=filter_city) if filter_city else ''
    section_from_filter = TechniqueSection.objects.get(name_slug=filter_section) if filter_section else ''
    subsection_from_filter = TechniqueSubSection.objects.get(name_slug=filter_subsection) if filter_subsection else ''

    if filter_city or filter_section or filter_subsection or filter_search or filter_h_from or filter_d_from:
        all_technique = filter_qs(all_technique_qs,
                                  filter_city,
                                  filter_section,
                                  filter_subsection,
                                  filter_search,
                                  filter_time_type,
                                  filter_h_from,
                                  filter_h_to,
                                  filter_h_price_from,
                                  filter_h_price_to,
                                  filter_d_from,
                                  filter_d_to,
                                  filter_d_price_from,
                                  filter_d_price_to
                                  )
    else:
        all_technique = all_technique_qs
    return render(request, 'catalog/catalog_inner.html', locals())

def technique_subsection_catalog(request, type_slug, section_slug, subsection_slug):
    current_technique_type = get_object_or_404(TechniqueType, name_slug=type_slug)
    current_technique_section = get_object_or_404(TechniqueSection, name_slug=section_slug)
    current_technique_subsection = get_object_or_404(TechniqueSubSection, name_slug=subsection_slug)

    seo_text = current_technique_subsection.seo_text
    all_technique_qs = TechniqueItem.objects.filter(sub_section=current_technique_subsection, is_moderated=True, is_active=True)
    filter_city = request.GET.get('city') if request.GET.get('city') != 'all' else None
    # filter_type = request.GET.get('type') if request.GET.get('type') != 'all' else None
    filter_section = request.GET.get('section') if request.GET.get('section') != 'all' else None
    filter_subsection = request.GET.get('subsection') if request.GET.get('subsection') != 'all' else None
    filter_search = request.GET.get('search') if request.GET.get('search') != '' else None

    filter_time_type = request.GET.get('time_type') if request.GET.get('time_type') != '' else None

    filter_h_from = request.GET.get('h_from') if request.GET.get('h_from') != '' else None
    filter_h_to = request.GET.get('h_to') if request.GET.get('h_to') != '' else None
    filter_h_price_from = request.GET.get('h_price_from') if request.GET.get('h_price_from') != '' else None
    filter_h_price_to = request.GET.get('h_price_to') if request.GET.get('h_price_to') != '' else None

    filter_d_from = request.GET.get('d_from') if request.GET.get('d_from') != '' else None
    filter_d_to = request.GET.get('d_to') if request.GET.get('d_to') != '' else None
    filter_d_price_from = request.GET.get('d_price_from') if request.GET.get('d_price_from') != '' else None
    filter_d_price_to = request.GET.get('d_price_to') if request.GET.get('d_price_to') != '' else None

    city_from_filter = City.objects.get(id=filter_city) if filter_city else ''
    section_from_filter = TechniqueSection.objects.get(name_slug=filter_section) if filter_section else ''
    subsection_from_filter = TechniqueSubSection.objects.get(name_slug=filter_subsection) if filter_subsection else ''

    if filter_city or filter_section or filter_subsection or filter_search or filter_h_from or filter_d_from:
        all_technique = filter_qs(all_technique_qs,
                                  filter_city,
                                  filter_section,
                                  filter_subsection,
                                  filter_search,
                                  filter_time_type,
                                  filter_h_from,
                                  filter_h_to,
                                  filter_h_price_from,
                                  filter_h_price_to,
                                  filter_d_from,
                                  filter_d_to,
                                  filter_d_price_from,
                                  filter_d_price_to
                                  )
    else:
        all_technique = all_technique_qs
    return render(request, 'catalog/catalog_inner.html', locals())


def technique(request, type_slug, section_slug, subsection_slug,technique_slug):
    techniqueItem = get_object_or_404(TechniqueItem, name_slug=technique_slug)
    if techniqueItem.owner != request.user:
        techniqueItem.views +=1
        techniqueItem.save()
    page_title = f'{techniqueItem.name} в аренду в {request.subdomain.cityAlias} по выгодным ценам, стоимость за час, за смену'
    page_description = f'{techniqueItem.name} в аренду в {request.subdomain.cityAlias} по низким ценам. Профессиональные водители, заправленная спецтехника и быстрая подача.'
    otherTechnique = TechniqueItem.objects.filter(owner=techniqueItem.owner).exclude(id=techniqueItem.id)
    all_feedbacks = TechniqueFeedback.objects.filter(techniqueitem=techniqueItem)

    return render(request, 'catalog/technique.html', locals())


def section_subscribe(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    print(request_body)
    try:
        sect_subscribe = SectionSubcribes.objects.get(section_id=request_body['section_id'])
        print('subcribe found')
    except:
        print('subcribe not found')
        sect_subscribe = SectionSubcribes.objects.create(section_id=request_body['section_id'])
    if (request_body['action'] == 'subscribe'):
        sect_subscribe.users.add(request.user)
        print('user added')
    if (request_body['action'] == 'unsubscribe'):
        sect_subscribe.users.remove(request.user)
        print('user removed')
    return JsonResponse({'status':'ok'}, safe=False)


def fast_search(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    print(request_body)
    return_dict = {}
    result_array = []


    sub_sections=TechniqueSubSection.objects.filter(name_lower__startswith=request_body['query'])
    sections = TechniqueSection.objects.filter(name_lower__startswith=request_body['query'])
    types = TechniqueType.objects.filter(name_lower__startswith=request_body['query'])
    print(sub_sections)
    print(sections)
    print(types)
    for i in sub_sections:
        result_array.append({
            'name': i.name,
            'path':f'&#10151; {i.section.name} &#10151; {i.section.type.name}',
            'url': f'{i.get_absolute_url()}'
        })
    for i in sections:
        result_array.append({
            'name': i.name,
            'path':f'&#10151;  {i.type.name}',
            'url': f'{i.get_absolute_url()}'
        })
    for i in types:
        result_array.append({
            'name': i.name,
            'path': '',
            'url': f'{i.get_absolute_url()}'
        })

    return_dict['result']=result_array
    return JsonResponse(return_dict, safe=False)