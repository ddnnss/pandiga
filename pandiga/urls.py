from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('staticPage.urls')),
    path('user/', include('customuser.urls')),
    path('', include('social_django.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
