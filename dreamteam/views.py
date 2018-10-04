from django.shortcuts import render, redirect
from account.models import *
from django.http import JsonResponse
from .models import *
from kichichi.shortcuts import *

# Create your views here.
def in_request(request):
    _from = request.user
    to = request.POST.get('username')
    _to = User.objects.get(username=to)
    if _to in _from.profile.demande.all():
        _from.profile.demande.remove(_to)
        notification = Notification.objects.get(user=_to, important=True, sender=_from)
        notification.delete()
        return JsonResponse({'success': True, 'remove':True,'add':False})
    if _to == dreamteampartern(_from):
        if _to.profil.langue == 'fr':
            Notification.objects.create(user=_to, notification=_from + ' s\'est rétiré du dream team')
        else:
            Notification.objects.create(user=_to, notification=_from + ' leaves the dream team')
        i = dreamteamid(_from)
        d = Dreamteam.objects.get(pk=i)
        d.delete()
        return JsonResponse({'success': True, 'remove': True, 'add': False})
    if _to.profile.langue == 'fr':
        Notification.objects.get_or_create(user=_to, notification=_from.username + ' veut former une dream team avec vous',
                                    sender=_from, important=True)
    elif _to.profile.langue == 'en':
        Notification.objects.get_or_create(user=_to, notification=_from.username + ' wants to form a dream team with you',
                                    sender=_from, important=True)
    _from.profile.demande.add(_to)
    return JsonResponse({'success': True, 'remove': False, 'add': True})

def in_yes(request):
    notification = request.POST.get('id')
    notification = Notification.objects.get(pk=int(notification))
    _from = notification.sender
    _to = notification.user
    for d in Dreamteam.objects.all():
        if d.member1 == _from or d.member2 == _from:
            other = None
            if d.member1 == _from:
                other = d.member2
            else:
                other = d.member1
            if other.profil.langue == 'fr':
                Notification.objects.create(user=other, notification=_from + ' s\'est rétiré du dream team')
            else:
                Notification.objects.create(user=other, notification=_from + ' leaves the dream team')
            d.delete()
        if d.member1 == _to or d.member2 == _to:
            other = None
            if d.member1 == _to:
                other = d.member2
            else:
                other = d.member1
            if other.profil.langue == 'fr':
                Notification.objects.create(user=other, notification=_to + ' s\'est rétiré du dream team')
            else:
                Notification.objects.create(user=d.member2, notification=_to + ' leaves the dream team')
            d.delete()
    dreamteam = Dreamteam.objects.create()
    dreamteam.member1 = _from
    dreamteam.member2 = _to
    dreamteam.save()
    _from.profile.demande.remove(_to)
    notification.delete()
    # Chat.objects.create(dreamteam=)
    return redirect('account:home')

def in_no(request):
    notification = request.POST.get('id')
    print(notification)
    notification = Notification.objects.get(notification=notification)
    _from = notification.sender
    _to = notification.user
    _from.demande.remove(_to)
    notification.delete()
    if _from.profil.langue == 'fr':
        Notification.objects.create(user=_from, notification=_to.username + ' a réjété votre demande')
    elif _from.profil.langue == 'en':
        Notification.objects.create(user=_from, notification=_to.username + ' has rejected your request')
    return JsonResponse({'success':True})


def chat(request):
    user = request.user
    dreamteam = Dreamteam.objects.get(pk=dreamteamid(user))
    _to = dreamteampartern(user)
    message = request.POST.get('chatwrite')
    Chat.objects.create(dreamteam=dreamteam, comefrom=user, to=_to, message=message, unread=True)
    return JsonResponse({'success':True, 'message':message})


def checkchat(request):
    user = request.user
    dreamteam = Dreamteam.objects.get(pk=dreamteamid(user))
    _to = dreamteampartern(user)
    count = 0
    for chat in Chat.objects.filter(dreamteam=dreamteam, comefrom=_to, unread=True):
        count = count + 1
    for chat in Chat.objects.filter(dreamteam=dreamteam, comefrom=_to, unread=True):
        chat.unread = False
        message = chat.message
        response = {
            'success':True,
            'message':message,
            'url':_to.profile.profil.url,
            'count':count,
        }
        chat.save()
        return JsonResponse(response)
    return JsonResponse({'success':False})