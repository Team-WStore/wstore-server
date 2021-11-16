from rest_framework import serializers

from .models import ItemCarrousel

class ItemCarrouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCarrousel
        fields = '__all__'