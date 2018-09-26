from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from account.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from kichichi.shorcuts import *

# Create your views here.
@login_required()
def main(request, user_name):
    device = device_type(request)
    lang = request.user.profile.langue
    if user_name != request.user.username:
        return HttpResponse("profile d'un autre utilisateur")
    user_profile = Profile.objects.get(user=request.user)
    publications = Publication.objects.all()[0:20]
    notifications = Notification.objects.filter(user=request.user)
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
        'profile': user_profile,
        'publications': publications,
        'notifications': notifications,
        'propositions': propositions,
        'followings': followings,
        'followings_first': followings_first,
        'followings_first_count': followings_first_count,
        'publications_counter': publications_counter,
        'lang':lang,
    }
    return render(request, '{0}/{1}/interface/user.html'.format(device, lang), context)

def delete_notification(request):
    if request.method == 'GET':
        raise Http404
    notification_id = request.POST.get('id')
    notification_id = int(notification_id)
    notification = Notification.objects.get(pk=notification_id).delete()
    user = request.user
    notification_number = Notification.objects.filter(user=user).count()
    data = {'success': True, 'id': notification_id, 'number': notification_number}
    return JsonResponse(data)