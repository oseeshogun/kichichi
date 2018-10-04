from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from account.views import home
from . import views

urlpatterns = [
    path('', home),

    path('demande/', views.in_request),

    path('yes/', views.in_yes),

    path('no/', views.in_no),

    path('chat/', views.chat),

    path('checkchat/', views.checkchat),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
