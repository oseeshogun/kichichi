from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from account.models import *
from dreamteam.models import *
from kichichi.shortcuts import *
from django.db.models import Q

# Create your views here.
@login_required()
def main(request, user_name):
    lang = request.user.profile.langue
    q = request.GET.get('q')
    a = request.GET.get('a')
    f = request.GET.get('f')
    if not a:
        a = False
    if not f:
        f = False
    publications = Publication.objects.all()[0:2]
    notifications = Notification.objects.filter(user=request.user)
    propositions = Profile.objects.all()
    if q:
        publications = Publication.objects.filter(
            Q(text__icontains=q) | Q(file__icontains=q)
        )[0:2]
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
    mypublications = Publication.objects.filter(publisher=request.user)[0:2]
    nomore = False
    if Publication.objects.filter(publisher=request.user)[0:2].count() <= 1:
        nomore = True
    myfollow = Following.objects.get(user=request.user)
    followings_count = myfollow.followings.count()
    if myfollow.followings.count() == 0:
        followings_count = 0
    abonnees = request.user.is_following_me.count()
    abs = request.user.is_following_me.all()
    if request.user.is_following_me.count() == 0:
        abonnees = 0
    context = {
        'lang':lang,
        'profile':request.user.profile,
        'notifications': notifications,
        'publications':publications,
        'propositions': propositions,
        'followings': followings,
        'followings_first': followings_first,
        'followings_first_count': followings_first_count,
        'publications_counter': publications_counter,
        'dreamteam':dreamteam,
        'partenaire':partenaire,
        'chats':chats,
        'abonnees':abonnees,
        'nomore':nomore,
        'followings_count':followings_count,
        'a':a,
        'f':f,
        'mypublications':mypublications,
    }
    return render(request, 'mobile/%s/interface/user.html' % lang, context)

@login_required()
def profile(request, user_name):
    if request.user.username == user_name:
        return redirect('mobile:mainmobile', user_name=user_name)
    try:
        user = User.objects.get(username=user_name)
    except User.DoesNotExist:
        raise Http404
    device = device_type(request)
    lang = request.user.profile.langue
    publications = Publication.objects.filter(publisher=user)[0:2]
    nomore = 'None'
    if Publication.objects.filter(publisher=user)[0:2].count() <= 1:
        nomore = True
    user_groups = User_groups.objects.filter(user=user)
    myfollow = Following.objects.get(user=user)
    followings = myfollow.followings.all()
    followings_count = myfollow.followings.count()
    if myfollow.followings.count() == 0:
        followings_count = 0
    abonnees = user.is_following_me.count()
    if user.is_following_me.count() == 0:
        abonnees = 0
    family = User_groups.objects.get(user=user, name='family')
    friends = User_groups.objects.get(user=user, name='friends')
    propositions = Profile.objects.all()
    myfollow = Following.objects.get(user=user)
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
    dreamteam = dreamteamid(request.user)
    partenaire = dreamteampartern(request.user)
    chats = False
    if dreamteam:
        dreamteam = Dreamteam.objects.get(pk=dreamteam)
        partenaire = dreamteampartern(request.user)
        for c in Chat.objects.filter(dreamteam=dreamteam, comefrom=partenaire, unread=True):
            c.unread = False
            c.save()
        chats = Chat.objects.filter(dreamteam=dreamteam).order_by('-sendtime')[:10]
    context = {
        'profile': request.user.profile,
        'publications': publications,
        'groups': user_groups,
        'followings': followings,
        'abonnees': abonnees,
        'followings_count': followings_count,
        'dreamteam': dreamteam,
        'family': family,
        'friends': friends,
        'lang': lang,
        'nomore': nomore,
        'propositions': propositions,
        'followings_first': followings_first,
        'followings_first_count': followings_first_count,
        'publications_counter': publications_counter,
        'user':user,
        'partenaire':partenaire,
        'chats':chats,
        'mobileprofile':True,
    }
    return render(request, '{0}/{1}/profil/soneprofil.html'.format(device, lang), context)
