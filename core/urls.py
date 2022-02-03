from django.urls import path

from .views import ItemCarrouselViewSet

core_patterns = ([
    path('slider/', ItemCarrouselViewSet.as_view()),
], 'core')