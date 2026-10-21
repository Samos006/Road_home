from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from road_home.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('users/', include("users.urls")),
    path('animals/', include("animals.urls")),
    path('events/', include("events.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
