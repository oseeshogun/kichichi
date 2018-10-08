from django.shortcuts import render, redirect
from account.models import *
from django.http import JsonResponse, Http404, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from datetime import datetime
from django.db.models import Q
from kichichi.shortcuts import *

# Create your views here.
def tokoss(request):
    if request.method == 'GET':
        raise Http404
    username = request.user.username
    publication_id = request.POST.get('publication_id')
    publication_id = int(publication_id)
    publication = Publication.objects.get(pk=publication_id)
    likers = publication.likers.all()
    unlike = False
    if request.user in likers:
        utilisateur = User.objects.get(username=username)
        actual_likes = publication.likes_number
        actual_likes = actual_likes - 1
        publication.likes_number = actual_likes
        publication.likers.remove(utilisateur)
        publication.save()
        unlike = True
    else:
        utilisateur = User.objects.get(username=username)
        publication.likers.add(utilisateur)
        actual_likes = publication.likes_number
        actual_likes = actual_likes + 1
        publication.likes_number = actual_likes
        publication.save()
        publisher = publication.publisher
        notification = str(utilisateur.username) + " a aimé votre publication ''" + publication.text + "''"
        if not publisher == request.user:
            if publisher.profile.langue == 'fr':
                Notification.objects.get_or_create(user=publisher, notification=notification)
            else:
                Notification.objects.get_or_create(user=publisher, notification=str(utilisateur.username) + " liked your publication ''" + publication.text + "''")
        if actual_likes == 100:
            notification = "Votre publication ''" + publication.text + "'' a atteint 100 tokoss, toutes nos félicitations"
            Notification.objects.get_or_create(user=publisher, notification=notification)
    data = {'success': True, 'likes': actual_likes, 'unlike': unlike}
    return JsonResponse(data)

def delete_publication(request):
    publication_id = request.POST.get('id')
    Publication.objects.get(pk=int(publication_id)).delete()
    user_name = request.user.username
    device = device_type(request)
    if device == 'pc':
        return redirect('profil:profil', user_name=user_name)
    if device == 'mobile':
        return redirect('mobile:mainmobile', user_name=user_name)

def inappropriate(request):
    if request.method == 'GET':
        raise Http404
    publication_id = request.POST.get('id')
    publication_id = int(publication_id)
    publication = Publication.objects.get(pk=publication_id)
    clicks = publication.inappropriate_clicks
    publication.inappropriate_clicks = clicks + 1
    publication.inappropriate = True
    user = request.user
    publication.inappropriate_clickers.add(user)
    publication.save()
    data = {'success':True}
    fs = FileSystemStorage()
    if publication.inappropriate_clicks >= 3:
        if publication.publisher.profile.langue == "fr":
            Notification.objects.create(user=publication.publisher, notification='Votre publication '+ publication.text +' a été supprimé puisqu\'elle est jugée inappropriée plusieurs fois')
        else:
            Notification.objects.create(user=publication.publisher, notification='Your publication '+ publication.text +' has been judged inappropriate severals times')
        fs.delete(publication.file)
        publication.delete()
    return JsonResponse(data)

def get_publication(request):
    response = {}
    start = request.GET.get('start')
    limit = request.GET.get('limit')
    start = int(start)
    limit = int(limit)
    q = request.GET.get('q')
    publications = Publication.objects.filter(public=True)[start:limit]
    if q != 'None':
        publications = Publication.objects.filter(
            Q(text__icontains=q) | Q(file__icontains=q)
        )[start:limit]
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
    if Publication.objects.filter(public=True)[start:limit + 1].count() <= 1:
        nomore = True
    if q != 'None':
        if Publication.objects.filter(Q(text__icontains=q) | Q(file__icontains=q))[start:limit + 1].count() <= 1:
            nomore = True
    if publications.count() != 0:
        for publication in publications:
            if request.user in publication.inappropriate_clickers.all():
                break
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
            publication_comment = Comments.objects.filter(publication=publication).first()
            comments_count = Comments.objects.filter(publication=publication).count()
            if publication_comment != None:
                comment_by = publication_comment.comment_by.username
                comment = publication_comment.comment
            if request.user.username == publication.publisher.username:
                is_him = True
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
                'liker': liker,
                'owner': owner,
                'comment_by': comment_by,
                'comment': comment,
                'comments_count': comments_count,
                'is_file':publication.is_file(),
                'is_him':is_him,
                'ads':ads,
                'tonot':False,
            }
            return JsonResponse(response)
    return JsonResponse({'tonot':True})


def addcomment(request):
    if request.method == 'GET':
        raise Http404
    publication_id = request.POST.get('publication_id')
    publication_id = int(publication_id)
    publication = Publication.objects.get(pk=publication_id)
    comment = request.POST.get('comment')
    user = request.user
    profil = Profile.objects.get(user=user)
    image = profil.profil.url
    Comments.objects.get_or_create(publication=publication, comment_by=user, comment=comment)
    comment_number = publication.comments_set.count()
    publisher = publication.publisher
    if not publisher == request.user:
        if publisher.profile.langue == 'fr':
            notification = str(user.username) + " a commenté votre publication ''" + publication.text +"''"
            Notification.objects.get_or_create(user=publisher, notification=notification)
        else:
            notification = str(user.username) + " has commented your publication ''" + publication.text +"''"
            Notification.objects.get_or_create(user=publisher, notification=notification)
    username = request.user.username
    data = {
        'success': True,
        'comment_number': comment_number,
        'id':publication_id,
        'comment':comment,
        'img': image,
        'username':username,
    }
    return JsonResponse(data)


def getcomments(request):
    lire_id = request.GET.get('publication')
    lire_id = lire_id.replace('lire', '')
    lire_id = int(lire_id)
    publication = Publication.objects.get(pk=lire_id)
    comments = Comments.objects.filter(publication=publication)
    data = {}
    comment_number = 0
    for comment in comments:
        comment_number = comment_number + 1
        user = comment.comment_by
        data['username' + str(comment_number)] = user.username
        data['url' + str(comment_number)] = user.profile.profil.url
        data['comment' + str(comment_number)] = comment.comment
    data['comment_number'] = comment_number
    data['id'] = lire_id
    return JsonResponse(data)

def poster(request):
    user_name = request.user.username
    device = device_type(request)
    if request.method == 'GET':
        raise Http404
    if request.method == 'POST' and request.FILES['file']:
        fs = FileSystemStorage()
        m = 0.0
        for pub in Publication.objects.all():
            m += pub.file.size / 1050030
        if m > 400:
            f = 0
            pub_to_delete = {}
            for pub in Publication.objects.all().order_by('launched'):
                f += pub.file.size / 1050030
                if not f <= 100:
                    f -= pub.file.size / 1050030
                    break
                pub_to_delete[pub.id] = pub
            for item in dict:
                if item.publisher.profile.langue == 'fr':
                    Notification.objects.create(user=item.publisher, notification='Votre publication '+ item.text +' a été récalée pour la gestion d\'espace de stockage pour la version beta, profitez-en pour poster plus de contenus.')
                else:
                     Notification.objects.create(user=item.publisher, notification='Your publication '+ item.text +' was deleted for the space storage management in the beta version, take the profit of it for publishing more content.')
                fs.delete(item.file)
                item.delete()
        text = request.POST.get('text')
        type = request.POST.get('type')
        public = request.POST.get('publication_group')
        file = request.FILES['file']
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
        filename = fs.save('Publication/' + str(year) + '/' + str(month) + '/' + str(day) + '/{0}'.format(file.name), file)
        uploaded_file_url = fs.url(filename)
        new_publication = Publication.objects.create(publisher=request.user, text=text, file=filename)
        new_publication.public = True
        new_publication.save()
        if device == 'pc':
            return redirect('profil:profil', user_name=user_name)
        if device == 'mobile':
            return redirect('mobile:mainmobile', user_name=user_name)
    return HttpResponse('Failed')
