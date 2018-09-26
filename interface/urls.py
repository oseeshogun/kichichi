from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from account.views import home

app_name = 'interface'

urlpatterns = [
    path('', home),

    path('delete/notification/', views.delete_notification),

    path('<slug:user_name>/', views.main, name='main'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
