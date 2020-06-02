from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from customuser.models import Notification
from technique.models import TechniqueItem
from techniqueOrder.models import TechniqueOrder
import json

def new_msg(request):
    print(request.POST == request.method)
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
        try:
            chat = Chat.objects.get(techniqueitem=techniqueItem)
        except:
            pass
        other_user = techniqueItem.owner
        print(chat)
        chat_type = body['chat_type']
    elif body['chat_type'] == 'order':
        techniqueOrder = get_object_or_404(TechniqueOrder, id=body['id'])
        try:
            chat = Chat.objects.get(order=techniqueOrder)
        except:
            pass
        other_user = techniqueOrder.customer
        chat_type = body['chat_type']

    # for x in chat:
    #     print('x=',x.id)
    #     c = Chat.objects.get(id = x.id)
    #     print(c.users.all())
    #     for u in c.users.all():
    #         if u == me:
    #             print('me')
    #             me_f = True
    #         if u == other_user:
    #             other_user_f =True
    #             if me_f:
    #                 chat_id = x.id
    #                 print('chat_id',chat_id)



    if chat:
        print('chat found')
        Message.objects.create(chat=chat,
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
    Notification.objects.create(user_id=body['msgTo'],
                                text='Новое сообщение в чате',
                                is_chat_notification=True,
                                redirect_url='/user/lk/?tab=tab-chat')
    return JsonResponse(return_dict, safe=False)



def get_msg(request):
    return_dict = {}
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    try:
        chat = Chat.objects.get(id=body['chat_id'])
    except:
        chat = None
    if chat:
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
                user_id = user_qs.id
                if chat.techniqueitem:
                    userInfo = {
                        'user_id': user_id,
                        'user_name': user_name,
                        'user_avatar': user_avatar,
                        'technique_img': chat.techniqueitem.images.first().image.url,
                        'technique_name': chat.techniqueitem.name[:10] + '...' if len(chat.techniqueitem.name) > 20 else chat.techniqueitem.name,
                        'technique_url': chat.techniqueitem.get_absolute_url()
                    }
                if chat.order:
                    if not request.user.is_customer:
                        userInfo = {
                            'user_id': user_id,
                            'user_name': user_name,
                            'user_avatar': user_avatar,
                            'technique_img': False,
                            'technique_name': f'Заявка № {chat.order.id}',
                            'technique_url': f'/technique/orders/{chat.order.name_slug}'
                        }
                    else:
                        userInfo = {
                            'user_id': user_id,
                            'user_name': user_name,
                            'user_avatar': user_avatar,
                            'technique_img': False,
                            'technique_name': f'Заявка № {chat.order.id}',
                            'technique_url': f'/user/lk/?tab=tab-my-order-detail&order_id={chat.order.id}'
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
    print(body)
    Message.objects.create(chat_id=body['chatId'], user_id=body['msgFrom'], message=body['msg'])
    # if int(body['msgFrom']) == request.user.id:
    #     chat_qs = Chat.objects.get(id=int(body['chatId']))
    #     chat_qs.lastMessageOwn = True
    #     chat_qs.save()
    chat_qs = Chat.objects.get(id=int(body['chatId']))
    chat_qs.lastMsgBy_id = request.user.id
    chat_qs.save()
    msg_to = None
    for u in chat_qs.users.all():
        if not u == request.user:
            msg_to = u

    Notification.objects.create(user=msg_to,
                                text='Новое сообщение в чате',
                                is_chat_notification=True,
                                redirect_url='/user/lk/?tab=tab-chat')
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
                user_id = user_qs.id
                user_activity = user_qs.get_user_activity(),

        if chat.techniqueitem :
            readChats.append({
                'is_read': chat.isNewMessages,
                'chat_id': chat.id,
                'user_id': user_id,
                'activity': user_activity,
                'chat_from': user_name,
                'user_avatar': user_avatar,
                'unread_mgs_count': len(chat.message_set.all().filter(isUnread=True)),
                'last_msg': chat.message_set.last().message,
                'last_msg_time': chat.message_set.last().createdAt.strftime("%d.%m.%Y,%H:%M:%S"),
                'technique_img': chat.techniqueitem.images.first().image.url,
                'technique_name': chat.techniqueitem.name[:10] + '...' if len(chat.techniqueitem.name) > 20 else chat.techniqueitem.name,
                'technique_url': chat.techniqueitem.get_absolute_url()

            })
        if chat.order :
            if request.user.is_customer:
                readChats.append({
                    'is_read': chat.isNewMessages,
                    'chat_id': chat.id,
                    'user_id': user_id,
                    'activity': user_activity,
                    'chat_from': user_name,
                    'user_avatar': user_avatar,
                    'unread_mgs_count': len(chat.message_set.all().filter(isUnread=True)),
                    'last_msg': chat.message_set.last().message,
                    'last_msg_time': chat.message_set.last().createdAt.strftime("%d.%m.%Y,%H:%M:%S"),
                    'technique_img': False,
                    'technique_name': f'Заявка № {chat.order.id}',
                    'technique_url': f'/technique/orders/{chat.order.name_slug}'

                })
            else:
                readChats.append({
                    'is_read': chat.isNewMessages,
                    'chat_id': chat.id,
                    'user_id': user_id,
                    'chat_from': user_name,
                    'activity': user_activity,
                    'user_avatar': user_avatar,
                    'unread_mgs_count': len(chat.message_set.all().filter(isUnread=True)),
                    'last_msg': chat.message_set.last().message,
                    'last_msg_time': chat.message_set.last().createdAt.strftime("%d.%m.%Y,%H:%M:%S"),
                    'technique_img': False,
                    'technique_name': f'Заявка № {chat.order.id}',
                    'technique_url': f'/user/lk/?tab=tab-my-order-detail&order_id={chat.order.id}'

                })


    print(readChats)
    return_dict['readChats'] = readChats
    return_dict['pages'] = allPages
    return JsonResponse(return_dict, safe=False)



def to_rent(request):
    if request.POST:
        techniqueItem = get_object_or_404(TechniqueItem,id=request.POST.get('techniqueItem_id'))
        chat = None
        try:
            chat = Chat.objects.get(techniqueitem=techniqueItem)
        except:
            pass
        print('chat=',chat)
        if chat:
            print('chat found')
            Message.objects.create(chat=chat,
                                   user=request.user,
                                   message=f'Привет, {request.POST.get("order_date")} хочу взять в аренду'
                                           f' {techniqueItem.name}, на {request.POST.get("rent_time")} {request.POST.get("rent_type")}')
            chat.lastMsgBy = request.user
            chat.save()
            Notification.objects.create(user=techniqueItem.owner,
                                        text=f'Запрос на аренду {techniqueItem.name} от {request.user.get_full_name()}',
                                        redirect_url='/user/lk/?tab=tab-notification')
        else:
            print('chat not found')
            Notification.objects.create(user=techniqueItem.owner,text=f'Запрос на аренду {techniqueItem.name} от {request.user.get_full_name()}',
                                        redirect_url='/user/lk/?tab=tab-notification')
            newChat = Chat.objects.create(techniqueitem=techniqueItem)
            newChat.users.add(request.user, techniqueItem.owner)

            newChat.lastMsgBy = request.user
            newChat.save()
            Message.objects.create(chat=newChat,user=request.user,
                                   message=f'Привет, {request.POST.get("order_date")} хочу взять в аренду'
                                           f' {techniqueItem.name}, на {request.POST.get("rent_time")} {request.POST.get("rent_type")}')

        return HttpResponseRedirect('/user/lk/?tab=tab-chat')


def delete_chat(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    chat_id = request_body['id']
    Chat.objects.get(id=chat_id).delete()
    return JsonResponse({'result': 'ok'})