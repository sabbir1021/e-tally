from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls' , namespace='shop')),
    path('accounts/', include('accounts.urls',namespace='accounts')),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.FORCE_STATIC_FILE_SERVING and not settings.DEBUG:
    settings.DEBUG = True
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    settings.DEBUG = False


admin.site.site_header = "tally khata"
admin.site.site_title = "tally khata Portal"
admin.site.index_title = "tally khata to Finder Researcher Portal"