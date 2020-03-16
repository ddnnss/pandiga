from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from technique.models import TechniqueItem
from techniqueOrder.models import TechniqueOrder
import json

def new_msg(request):
    return_dict = {}
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    chat = None
    chat_found = False
    chat_type = ''
    techniqueItem = None
    techniqueOrder = None
    me = request.user
    me_f = False
    other_user = None
    other_user_f = False
    chat_id=0
    print(body)
    if body['chat_type'] == 'tech':
        techniqueItem = get_object_or_404(TechniqueItem, id=body['id'])
        chat = Chat.objects.filter(users__in=[techniqueItem.owner, request.user])
        other_user = techniqueItem.owner
        print(chat)
        chat_type = body['chat_type']
    elif body['chat_type'] == 'order':
        techniqueOrder = get_object_or_404(TechniqueOrder, id=body['id'])
        chat = Chat.objects.filter(users__in=[techniqueOrder.customer, request.user])
        other_user = techniqueOrder.customer
        chat_type = body['chat_type']

    for x in chat.all():
        print('x=',x.id)
        c = Chat.objects.get(id = x.id)
        print(c.users.all())
        for u in c.users.all():
            if u == me:
                print('me')
                me_f = True
            if u == other_user:
                other_user_f =True
                if me_f:
                    chat_id = x.id
                    print('chat_id',chat_id)



    if me_f and other_user_f:
        print('chat found')
        Message.objects.create(chat_id=chat_id,
                               user=request.user,
                               message=body['msg'])
    else:
        print('chat not found')
        newChat = None
        if chat_type == 'tech':
            newChat = Chat.objects.create(techniqueitem=techniqueItem)
            newChat.users.add(request.user, techniqueItem.owner)
        elif chat_type == 'order':
            newChat = Chat.objects.create(order=techniqueOrder)
            newChat.users.add(request.user, techniqueOrder.customer)

        # if int(body['msgFrom']) == request.user.id:
        #     newChat.lastMessageOwn = True
        #     newChat.save()
        newChat.lastMsgBy_id = request.user.id
        newChat.save()
        Message.objects.create(chat=newChat, user=request.user,
                               message=body['msg'])
    # Message.objects.create(messageTo_id=body['msgTo'],messageFrom_id=body['msgFrom'],message=body['msg'])
    return_dict['result'] = 'ok'
    return JsonResponse(return_dict, safe=False)



def get_msg(request):
    return_dict = {}
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    chat = Chat.objects.get(id=body['chat_id'])

    if not chat.lastMsgBy == request.user:
        chat.isNewMessages = False
        chat.save()
    userInfo ={}
    chatMsg = []
    for user in chat.users.all():
        if user.id != request.user.id:
            user_qs = User.objects.get(id=user.id)
            user_name = user_qs.first_name
            user_avatar = user_qs.get_avatar()
            userInfo = {
                'user_name': user_name,
                'user_avatar': user_avatar,
                'technique_img': chat.techniqueitem.images.first().image.url,
                'technique_name': chat.techniqueitem.name,
                'technique_url': chat.techniqueitem.get_absolute_url()

            }
    for x in chat.message_set.all():
        chatItem = {}
        chatItemInner = []
        print('user', x.user.id)
        if x.user == request.user:
            x.isUnread = False
            x.save()
        if x.user == request.user:
            chatItem['own'] = [x.message, x.createdAt.strftime("%d.%m.%Y,%H:%M:%S")]
        else:
            chatItem['from'] = [x.message, x.createdAt.strftime("%d.%m.%Y,%H:%M:%S")]
        chatMsg.append(chatItem)
    return_dict['userInfo'] = userInfo
    return_dict['chatMsg'] = chatMsg
    return JsonResponse(return_dict,safe=False)


def add_msg(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    Message.objects.create(chat_id=body['chatId'], user_id=body['msgFrom'], message=body['msg'])
    # if int(body['msgFrom']) == request.user.id:
    #     chat_qs = Chat.objects.get(id=int(body['chatId']))
    #     chat_qs.lastMessageOwn = True
    #     chat_qs.save()
    chat_qs = Chat.objects.get(id=int(body['chatId']))
    chat_qs.lastMsgBy_id = request.user.id
    chat_qs.save()
    return JsonResponse('ok',safe=False)


def get_chats(request):
    return_dict = {}
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    allChats_temp = Chat.objects.filter(users__in=[request.user.id]).order_by('-updatedAt')

    chats_paginator = Paginator(allChats_temp, 5)



    try:
        allChats = chats_paginator.get_page(body['page'])
    except PageNotAnInteger:
        allChats = chats_paginator.page(1)
    except EmptyPage:
        allChats = chats_paginator.page(chats_paginator.num_pages)



    readChats = []
    allPages = {'last_page': chats_paginator.num_pages, 'curent_page': body['page']}
    unread_count = 0
    for chat in allChats:


        print('unread_count', chat.message_set.filter(isUnread=True).count)
        user_name = ''
        user_avatar = ''
        for user in chat.users.all():
            if user.id != request.user.id:
                user_qs = User.objects.get(id=user.id)
                user_name = user_qs.first_name
                user_avatar = user_qs.get_avatar()

        readChats.append({
            'chat_id': chat.id,
            'chat_from': user_name,
            'user_avatar': user_avatar,
            'unread_mgs_count': len(chat.message_set.all().filter(isUnread=True)),
            'last_msg': chat.message_set.last().message,
            'last_msg_time': chat.message_set.last().createdAt.strftime("%d.%m.%Y,%H:%M:%S"),
            'technique_img': chat.techniqueitem.images.first().image.url,
            'technique_name': chat.techniqueitem.name,
            'technique_url': chat.techniqueitem.get_absolute_url()

        })
    print(readChats)
    return_dict['readChats'] = readChats
    return_dict['pages'] = allPages
    return JsonResponse(return_dict, safe=False)



def to_rent(request,item_id):
    techniqueItem = get_object_or_404(TechniqueItem,id=item_id)
    chat = Chat.objects.filter(users__in=[techniqueItem.owner, request.user])
    me = request.user
    me_f = False
    other_user = None
    other_user_f = False
    chat_id = 0
    for x in chat.all():
        print('x=',x.id)
        c = Chat.objects.get(id = x.id)
        print(c.users.all())
        for u in c.users.all():
            if u == me:
                print('me')
                me_f = True
            if u == other_user:
                other_user_f =True
                if me_f:
                    chat_id = x.id
                    print('chat_id',chat_id)



    if me_f and other_user_f:
        print('chat found')
        Message.objects.create(chat_id=chat_id,
                               user=request.user,
                               message='Привет, хочу взять технику в аренду')
    else:
        print('chat not found')
        newChat = Chat.objects.create(techniqueitem=techniqueItem)
        newChat.users.add(request.user, techniqueItem.owner)
        # if int(body['msgFrom']) == request.user.id:
        #     newChat.lastMessageOwn = True
        #     newChat.save()
        newChat.lastMsgBy_id = request.user.id
        newChat.save()
        Message.objects.create(chat=newChat,user=request.user,
                               message='Привет, хочу взять технику в аренду')
    # Message.objects.create(messageTo_id=body['msgTo'],messageFrom_id=body['msgFrom'],message=body['msg'])
    return HttpResponseRedirect('/user/lk/?tab=tab-chat')