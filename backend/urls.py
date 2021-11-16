from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from product.urls import product_patterns

urlpatterns = [
    # product
    path("api/v1/", include(product_patterns)),
    path('admin/', admin.site.urls),

    # Rest auth
    path('api/v1/auth/',
         include('rest_auth.urls')),
    path('api/v1/auth/registration/',
         include('rest_auth.registration.urls')),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)