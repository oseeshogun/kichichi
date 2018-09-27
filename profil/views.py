from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from account.models import *
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from datetime import datetime
from kichichi.shorcuts import *

# Create your views here.
@login_required()
def profil(request, user_name):
    if request.user.username == user_name:
        return redirect('profil:myprofile')
    user = User.objects.get(username=user_name)
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
    abonnees = request.user.is_following_me.count()
    if request.user.is_following_me.count() == 0:
        abonnees = 0
    dreamteam = User_groups.objects.get(user=user, name='dreamteam')
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
    }
    return render(request, '{0}/{1}/profil/soneprofil.html'.format(device, lang), context)


@login_required()
def myprofil(request):
    device = device_type(request)
    lang = request.user.profile.langue
    publications = Publication.objects.filter(publisher=request.user)[0:2]
    nomore = 'None'
    if Publication.objects.filter(publisher=request.user)[0:2].count() <= 1:
        nomore = True
    user_groups = User_groups.objects.filter(user=request.user)
    myfollow = Following.objects.get(user=request.user)
    followings = myfollow.followings.all()
    followings_count = myfollow.followings.count()
    if myfollow.followings.count() == 0:
        followings_count = 0
    abonnees = request.user.is_following_me.count()
    if request.user.is_following_me.count() == 0:
        abonnees = 0
    dreamteam = User_groups.objects.get(user=request.user, name='dreamteam')
    family = User_groups.objects.get(user=request.user, name='family')
    friends = User_groups.objects.get(user=request.user, name='friends')
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
    }
    return render(request, '{0}/{1}/profil/profil.html'.format(device, lang), context)

def change_profil(request):
    if request.method == 'GET':
        raise Http404
    user_name = request.user.username
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        file_name = 'profil_' + user_name + '.jpg'
        filename = fs.save('profiles/user_{0}/{1}'.format(request.user.username, file_name), file)
        uploaded_file_url = fs.url(filename)
        user_profile = Profile.objects.get(user=request.user)
        user_profile.profil = filename
        user_profile.save()
        return redirect('profil:profil', user_name=user_name)
    return redirect('profil:profil', user_name=user_name)


def getpublication(request):
    username = request.GET.get('username')
    start = request.GET.get('start')
    limit = request.GET.get('limit')
    response = {}
    start = int(start)
    limit = int(limit)
    user = User.objects.get(username=username)
    publications = Publication.objects.filter(publisher=user)[start:limit]
    size = False
    audio = False
    video = False
    image = False
    nomore = False
    liker = False
    owner = False
    comment_by = False
    comment = False
    is_him = False
    if Publication.objects.filter(publisher=user)[start:limit + 1].count() <= 1:
        nomore = True
    if publications.count() != 0:
        for publication in publications:
            if publication.is_file():
                size = publication.size()
            if publication.file.name.lower().endswith('.mp3') or publication.file.name.lower().endswith('.aac'):
                audio = publication.file.url
            elif publication.file.name.lower().endswith('.mp4'):
                video = publication.file.url
            else:
                image = publication.file.url
            likes_number = publication.likes_number
            if request.user in publication.likers.all():
                liker = True
            if request.user.username == publication.publisher.username:
                owner = True
            publication_comment = Comments.objects.filter(publication=publication).last()
            comments_count = Comments.objects.filter(publication=publication).count()
            if publication_comment != None:
                comment_by = publication_comment.comment_by.username
                comment = publication_comment.comment
            if request.user.username == publication.publisher.username:
                is_him = True
            response = {
                'id': publication.id,
                'profil': publication.publisher.profile.profil.url,
                'publisher': publication.publisher.username,
                'text': publication.text,
                'size': str(size),
                'audio': audio,
                'video': video,
                'image': image,
                'likes_number': likes_number,
                'nomore': nomore,
                'liker': liker,
                'owner': owner,
                'comment_by': comment_by,
                'comment': comment,
                'comments_count': comments_count,
                'is_file': publication.is_file(),
                'is_him': is_him,
            }
            return JsonResponse(response)
    return JsonResponse(response)


def updateprofil(request):
    user_name = request.user.username
    town = request.POST.get('town')
    country = request.POST.get('country')
    profession = request.POST.get('profession')
    birthday = request.POST.get('birthday')
    profile = Profile.objects.get(user=request.user)
    profile.town = town
    profile.country = country
    profile.profession = profession
    if birthday:
        profile.birthday = birthday
    profile.save()
    return redirect('profil:profil', user_name=user_name)



def followprofil(request):
    if request.method == 'GET':
        raise Http404
    username = request.POST.get('username')
    user = request.user
    profil_username = request.POST.get('username')
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