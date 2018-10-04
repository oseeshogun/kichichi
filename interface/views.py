from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from account.models import *
from dreamteam.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from kichichi.shortcuts import *
from django.db.models import Q

# Create your views here.
@login_required()
def main(request, user_name):
    device = device_type(request)
    lang = request.user.profile.langue
    if user_name != request.user.username:
        return redirect('profil:profil', user_name=user_name)
    user_profile = Profile.objects.get(user=request.user)
    publications = Publication.objects.all()[0:2]
    notifications = Notification.objects.filter(user=request.user)[:10]
    propositions = Profile.objects.all()
    myfollow = Following.objects.get(user=request.user)
    followings = myfollow.followings.all()
    followings_first = {}
    for e in myfollow.followings.all():
        hisfollow = Following.objects.get(user=e)
        his_list = hisfollow.followings.all()
        for i in his_list:
            followings_first[i.username] = i
    publications_counter = 0
    followings_first_count = 0
    for proposition in propositions:
        if not proposition.user in followings:
            if proposition.user.username in followings_first:
                followings_first_count = followings_first_count + 1
    superusers = User.objects.filter(is_superuser=True)
    dreamteam = dreamteamid(request.user)
    partenaire = " "
    chats = False
    if dreamteam:
        dreamteam = Dreamteam.objects.get(pk=dreamteam)
        partenaire = dreamteampartern(request.user)
        for c in Chat.objects.filter(dreamteam=dreamteam, comefrom=partenaire, unread=True):
            c.unread = False
            c.save()
        chats = Chat.objects.filter(dreamteam=dreamteam).order_by('-sendtime')[:10]
    context = {
        'profile': user_profile,
        'publications': publications,
        'notifications': notifications,
        'propositions': propositions,
        'followings': followings,
        'followings_first': followings_first,
        'followings_first_count': followings_first_count,
        'publications_counter': publications_counter,
        'lang':lang,
        'superusers':superusers,
        'dreamteam':dreamteam,
        'partenaire':partenaire,
        'chats':chats,
    }
    return render(request, '{0}/{1}/interface/user.html'.format(device, lang), context)

def delete_notification(request):
    if request.method == 'GET':
        raise Http404
    notification_id = request.POST.get('id')
    notification_id = int(notification_id)
    notification = Notification.objects.get(pk=notification_id)
    if notification.important:
        _from = notification.sender
        _to = notification.user
        _from.profile.demande.remove(_to)
        if _from.profile.langue == 'fr':
            Notification.objects.create(user=_from, notification=_to.username + ' a réjété votre demande')
        elif _from.profile.langue == 'en':
            Notification.objects.create(user=_from, notification=_to.username + ' has rejected your request')
    notification = Notification.objects.get(pk=notification_id).delete()
    user = request.user
    notification_number = Notification.objects.filter(user=user).count()
    data = {'success': True, 'id': notification_id, 'number': notification_number}
    return JsonResponse(data)


def follow(request):
    if request.method == 'GET':
        raise Http404
    user = request.user
    profil_username = request.POST.get('profil_username')
    type = request.POST.get('type')
    data = {}
    lang = request.user.profile.langue
    to_add_user = User.objects.get(username=profil_username)
    myfollow = Following.objects.get(user=user)
    followings = myfollow.followings.all()
    if not to_add_user in followings:
        myfollow.followings.add(to_add_user)
        data['success'] = 'Unfollow'
        if lang == 'fr':
            data['text'] = 'Ne plus suivre'
        elif lang == 'en':
            data['text'] = 'Unfollow'
    else:
        myfollow.followings.remove(to_add_user)
        data['success'] = 'follow'
        if lang == 'fr':
            data['text'] = 'Suivre'
        elif lang == 'en':
            data['text'] = 'Follow'
    return JsonResponse(data)

@login_required()
def search(request):
    q = request.GET.get('q')
    device = device_type(request)
    lang = request.user.profile.langue
    user_profile = Profile.objects.get(user=request.user)
    publications = Publication.objects.filter(
        Q(text__icontains=q) | Q(file__icontains=q)
    )[0:2]
    nomore =False
    if Publication.objects.filter(Q(text__icontains=q) | Q(file__icontains=q))[0:3].count() <= 2:
        nomore = True
    notifications = Notification.objects.filter(user=request.user)[:10]
    propositions = Profile.objects.filter(
        Q(user__username__icontains=q)
    )
    myfollow = Following.objects.get(user=request.user)
    followings = myfollow.followings.all()
    followings_first = {}
    for e in myfollow.followings.all():
        hisfollow = Following.objects.get(user=e)
        his_list = hisfollow.followings.all()
        for i in his_list:
            followings_first[i.username] = i
    publications_counter = 0
    followings_first_count = 0
    for proposition in propositions:
        if not proposition.user in followings:
            if proposition.user.username in followings_first:
                followings_first_count = followings_first_count + 1
    superusers = User.objects.filter(is_superuser=True)
    dreamteam = dreamteamid(request.user)
    partenaire = " "
    chats = False
    if dreamteam:
        dreamteam = Dreamteam.objects.get(pk=dreamteam)
        partenaire = dreamteampartern(request.user)
        for c in Chat.objects.filter(dreamteam=dreamteam, comefrom=partenaire, unread=True):
            c.unread = False
            c.save()
        chats = Chat.objects.filter(dreamteam=dreamteam).order_by('-sendtime')[:10]
    context = {
        'profile': user_profile,
        'publications': publications,
        'notifications': notifications,
        'propositions': propositions,
        'followings': followings,
        'followings_first': followings_first,
        'followings_first_count': followings_first_count,
        'publications_counter': publications_counter,
        'lang': lang,
        'superusers': superusers,
        'nomore':nomore,
        'dreamteam':dreamteam,
        'partenaire':partenaire,
        'chats':chats,
    }
    return render(request, '{0}/{1}/interface/user.html'.format(device, lang), context)