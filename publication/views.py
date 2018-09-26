from django.shortcuts import render
from account.models import *
from django.http import JsonResponse, Http404



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
            Notification.objects.get_or_create(user=publisher, notification=notification)
        if actual_likes == 100:
            notification = "Votre publication ''" + publication.text + "'' a atteint 100 tokoss, toutes nos félicitations"
            Notification.objects.get_or_create(user=publisher, notification=notification)
    data = {'success': True, 'likes': actual_likes, 'unlike': unlike}
    return JsonResponse(data)

def delete_publication(request):
    publication_id = request.POST.get('id')
    Publication.objects.get(pk=int(publication_id)).delete()
    return redirect('profil:profil', user_name=request.user.username)

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
    return JsonResponse(data)

def get_publication(request):
    response = {}
    start = request.GET.get('start')
    limit = request.GET.get('limit')
    start = int(start)
    limit = int(limit)
    q = request.GET.get('q')
    publications = Publication.objects.filter(public=True)[start:limit]
    size = False
    audio = False
    video = False
    image = False
    nomore = False
    liker = False
    owner = False
    comment_by = False
    comment = False
    if Publication.objects.filter(public=True)[start:limit + 1].count() <= 1:
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
            publication_comment = Comments.objects.last()
            comments_count = Comments.objects.all().count()
            if publication_comment != None:
                comment_by = publication_comment.comment_by
                comment = publication_comment.comment
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
            }
            return JsonResponse(response)
    return JsonResponse(response)