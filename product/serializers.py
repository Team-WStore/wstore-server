from rest_framework import serializers

from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth=2

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['user']
        depth=2

class ItemOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ['user']
        depth=2

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'