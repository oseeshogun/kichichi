from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('tokoss/', views.tokoss),

    path('delete/', views.delete_publication),

    path('inappropriate/', views.inappropriate),

    path('get/', views.get_publication),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
