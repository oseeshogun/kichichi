from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from account.views import home
from . import views

urlpatterns = [
    path('inrequest/', views.in_request),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
