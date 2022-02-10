from attr import fields
from rest_framework import serializers

from .models import Address, Brand, Category, Payment, Product, Order, OrderItem, WishlistItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
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
        depth=3

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
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['user']
        depth=1

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ['user']
        depth=1

class OrderSerializer(serializers.ModelSerializer):

    shipping_address = AddressSerializer()
    payment = PaymentSerializer()
    products = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        exclude=['user']
        depth=2