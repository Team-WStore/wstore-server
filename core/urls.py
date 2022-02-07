from django.urls import path

from .views import ItemCarrouselCreate, ItemCarrouselUpdateDelete, ItemCarrouselViewSet, ItemImageUpdateDelete, ItemImageView

core_patterns = ([
    path('slider/', ItemCarrouselViewSet.as_view()),
    path('slider-modify/<int:pk>', ItemCarrouselUpdateDelete.as_view()),
    path('slider-modify/', ItemCarrouselCreate.as_view()),
    path('image/', ItemImageView.as_view()),
    path('image-modify/<int:pk>', ItemImageUpdateDelete.as_view()),
], 'core')