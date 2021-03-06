from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from .models import *
#the validator.py is contain sign up  user validations form
from . import validator
from django.contrib.auth import login, authenticate, logout
from kichichi.shortcuts import device_type
from django.contrib.auth.views import LogoutView
import datetime
from datetime import timezone
from kichichi.shortcuts import *
from dreamteam.models import *
# Create your views here.
# Create your views here.


langues = ['en', 'fr']  #these are supported languages in kichichi


#the home view is used to redirect the user when he enters in kichichi.com
def home(request):
    lang = 'fr'
    if request.user.is_authenticated:
        username = request.user.username
        if device_type(request) == 'mobile':
            return redirect('mobile:mainmobile', user_name=username)
        #if the user is authenticated, he's redirect to the interface
        return redirect('interface:main', user_name=username)
    #if the user is unknown, he's is redirect to the anonymous page with french like default language
    return redirect('account:anonymous', lang=lang)

def anonymous(request, lang):
    if request.user.is_authenticated:
        username = request.user.username
        # if the user is authenticated, he's redirect to the interface
        return redirect('interface:main', user_name=username)
    if not lang in langues:
        raise Http404
    device = device_type(request)
    publications = Publication.objects.filter(public=True)[0:2]
    search = request.GET.get('q')
    finished = False
    if search:
        publications = Publication.objects.filter(public=True, text__icontains=search)[0:2]
        if Publication.objects.filter(public=True, text__icontains=search)[0:3].count() <= 2:
            finished = True
    context = {
        'publications': publications,
        'finished': finished,
        'lang': lang,
    }
    response = render(request, '{0}/{1}/registration/anonymous.html'.format(device, lang), context)
    response.set_cookie('current_lang', lang)
    return response


def login_user(request):
    if request.method == 'GET':
        raise Http404
    reponse = {}
    username = request.POST['username']
    password = request.POST['password']
    try:
        superuser = User.objects.get(username=username)
        if not superuser.is_superuser:
            password = validator.salting_password(password)
    except User.DoesNotExist:
        pass
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        reponse['success'] = 'success'
    else:
        try:
            user = User.objects.get(username=username)
            reponse['erroronpassword'] = 'erroronpassword'
        except User.DoesNotExist:
            pass
        reponse['error'] = 'error'
    return JsonResponse(reponse)

def signup_user(request):
    if request.method == 'GET':
        raise Http404
    data = {}
    username = request.POST.get('username')
    contact = request.POST.get('contact')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    lang = request.POST.get('langue')
    if not validator.valid_username(username):
        data['valid_username'] = "not_valid_username"
    if validator.username_exist(username):
        data['username_exist'] = 'username_exist'
    if not validator.passwords_match(password1, password2):
        data['passwords_match'] = 'not_passwords_match'
    if not validator.valid_contact_email(contact) == 'Not email':
        if not validator.valid_contact_email(contact):
            data['valid_contact_email'] = 'valid_contact_email'
        if validator.existing_mail_address(contact):
            data['existing_mail_address'] = 'existing_mail_address'
    else:
        if not validator.valid_contact_phone_number(contact):
            data['valid_contact_phone_number'] = 'valid_contact_phone_number'
        if validator.existing_phone_number(contact):
            data['existing_phone_number'] = 'existing_phone_number'
    if not validator.valid_password(password1):
        data['valid_password'] = 'valid_password'
    if len(data) == 0:
        password1 = validator.salting_password(password1)
        new_user = User.objects.create_user(username=username, password=password1)
        if '@' in contact:
            new_user.email = contact
        new_user.save()
        new_profile = Profile.objects.create(user=new_user)
        new_profile.langue = lang
        if not '@' in contact:
            new_profile.phone_number = contact
        new_profile.save()
        Following.objects.create(user=new_user)
        Onliners.objects.create(user=new_user)
        login(request, new_user)
        initial_groups = ['dreamteam', 'family', 'friends']
        for group in initial_groups:
            User_groups.objects.create(user=new_user, name=group)
        notification = " "
        if lang == "fr":
            notification = """Cette version est un bêta, il y a des fonctionnalités à complèter,
                                pour l'instant, nous
                                vous prions de notifier chaque remarque, critique ou erreur sur Kichichi, Merci. 
                                Mbula Mboma Gilberto (équipe de developpement)"""
            Notification.objects.get_or_create(user=new_user, notification=notification)
            notification = "Bienvenue sur Kichichi, nous sommes ravis de vous savoir connecter"
            Notification.objects.get_or_create(user=new_user, notification=notification)
        else:
            notification = """This is a beta version, There are features to complete,
                                            for the time being, we
                                            beg you to notify each remark, critic or mistake on Kichichi, Thank you. 
                                            Mbula Mboma Gilberto (development team)"""
            Notification.objects.get_or_create(user=new_user, notification=notification)
            notification = "Welcome to Kichichi, We are happy to see you connected"
            Notification.objects.get_or_create(user=new_user, notification=notification)
        data['success'] = 'success'
    return JsonResponse(data)



def get_publications(request):
    start = request.GET.get('start')
    limit = request.GET.get('limit')
    start = int(start)
    limit = int(limit)
    q = request.GET.get('q')
    publications = Publication.objects.filter(public=True)[start:limit]
    if q != 'None':
        publications = Publication.objects.filter(public=True, text__icontains=q)[start:limit]
    size = 'None'
    audio = 'None'
    video = 'None'
    image = 'None'
    nomore = 'None'
    if q != 'None':
        if Publication.objects.filter(public=True, text__icontains=q)[start:limit + 1].count() == 1:
            nomore = True
    else:
        if Publication.objects.filter(public=True)[start:limit + 1].count() == 1:
            nomore = True
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
        ads = False
        if start % 8 == 0:
            ads = True
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
            'ads':ads,
        }
        return JsonResponse(response)



def logout_user(request):
    logout(request)
    return redirect('account:home')

def online(request):
    online = Onliners.objects.get(user=request.user)
    online.online = True
    online.save()
    for online in Onliners.objects.all():
        if datetime.datetime.now(timezone.utc) - online.intime > datetime.timedelta(0, 15, 685252):
            online.online = False
            online.save()
    dreamteam = dreamteamid(request.user)
    if dreamteam:
        partenaire = dreamteampartern(request.user)
        online = partenaire.onliners.online
    else:
        online = False
    return JsonResponse({'online':online})

def message(request):
    message = request.POST.get('message')
    Message.objects.create(user=request.user, message=message)
    return JsonResponse({'success':True})