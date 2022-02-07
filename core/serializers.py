from rest_framework import serializers

from .models import ImageItem, ItemCarrousel

class ItemCarrouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCarrousel
        fields = '__all__'


class ImageItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageItem
        fields = '__all__'