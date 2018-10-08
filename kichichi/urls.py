from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from account.views import home

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home),

    #this path is for accounts: it conatains login, signup  and anonymous views
    path('accounts/', include('account.urls')),

    path('user/', include('interface.urls')),

    path('publication/', include('publication.urls')),

    path('profile/', include('profil.urls')),

    path('dreamteam/', include('dreamteam.urls')),

    path('mobile/', include('mobile.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
