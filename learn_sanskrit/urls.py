from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('learn-sanskrit/',include('sanskrit.urls',namespace='sanskrit')),
    path('learn-sanskrit/forums/', include('forums.urls',namespace='forums')),
    path('learn-sanskrit/accounts/',include('accounts.urls',namespace='accounts')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)