from django.urls import path

from .views import ItemCarrouselCreate, ItemCarrouselUpdateDelete, ItemCarrouselViewSet

core_patterns = ([
    path('slider/', ItemCarrouselViewSet.as_view()),
    path('slider-modify/<int:pk>', ItemCarrouselUpdateDelete.as_view()),
    path('slider-modify/', ItemCarrouselCreate.as_view()),
], 'core')