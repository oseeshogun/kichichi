from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from account.views import home
from . import views

app_name = 'mobile'

urlpatterns = [
    path('', home),

    path('profile/<slug:user_name>/', views.profile),

    path('<slug:user_name>/', views.main, name='mainmobile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
