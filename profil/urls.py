from django.contrib import admin
from django.urls import path, include
from account.views import home
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = 'profil'

urlpatterns = [
    path('', views.myprofil, name='myprofile'),

    path('change/', views.change_profil),

    path('getpublication/', views.getpublication),

    path('update/', views.updateprofil),

    path('follow/', views.followprofil),

    path('note/', views.note),

    path('<slug:user_name>/', views.profil, name='profil')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)