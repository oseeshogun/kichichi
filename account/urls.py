from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'account'

urlpatterns = [
    path('', views.home, name='home'),

    path('anonymous/<slug:lang>/', views.anonymous, name='anonymous'),

    path('login/', views.login_user,name='login'),


    path('signup/', views.signup_user, name='login'),

    path('get-publications/', views.get_publications),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)