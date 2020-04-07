from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('staticPage.urls')),
    path('user/', include('customuser.urls')),
    path('catalog/', include('technique.urls')),
    path('chat/', include('chat.urls')),
    path('technique/', include('techniqueOrder.urls')),
    path('pay/', include('ya_payment.urls')),
    path('partner/', include('partner.urls')),
    path('tarif/', include('tariff.urls')),
    path('feedback/', include('feedback.urls')),
    path('', include('social_django.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
