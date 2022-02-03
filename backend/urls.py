from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from product.urls import product_patterns
from core.urls import core_patterns
from userdata.views import HandleProfile

urlpatterns = [
    # product
    path("api/v1/", include(product_patterns)),
    # core
    path("api/v1/", include(core_patterns)),

    path('admin/', admin.site.urls),
    # profile
    path("api/v1/profile/", HandleProfile.as_view()),

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