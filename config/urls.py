from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls', namespace='core')),
    path('catalog/', include('apps.catalog.urls', namespace='catalog')),
    path('gallery/', include('apps.gallery.urls', namespace='gallery')),
    path('reviews/', include('apps.reviews.urls', namespace='reviews')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('crm/', include('apps.crm.urls', namespace='crm')),
    # App URLs will be included here
    # path('', include('apps.core.urls')),
    # path('catalog/', include('apps.catalog.urls')),
    # ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
