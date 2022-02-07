from attr import fields
from rest_framework import serializers

from .models import Brand, Category, Product, Order, OrderItem, WishlistItem

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
        exclude = ['user']
        depth=2

class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        exclude = ['user']
        depth=2

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        depth=1

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
        depth=1