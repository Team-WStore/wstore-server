from copy import copy
from numpy import product
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import mixins, generics
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.conf import settings

from .models import Brand, Category, Payment, Product, Order, Address, OrderItem, WishlistItem
from core.models import ImageItem
from .serializers import CategorySerializer, OrderItemSerializer, ProductSerializer, OrderSerializer, ItemOrderSerializer, WishlistItemSerializer

from rest_framework import status

# Create your views here.

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class CategoryView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request):
        return self.list(request)

class HandleProduct(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request):
        return self.list(request)

class HandleProductP(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

class ItemProductCreate(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def post(self, request):
        name = request.data.get('name')
        brand = request.data.get('brand')
        price = request.data.get('price')
        discount = request.data.get('discount')
        category = request.data.get('category')
        images = request.data.get('images', [])
        available = request.data.get('available')

        product = Product.objects.create(
            name=name,
            brand=Brand.objects.get(id=brand),
            price=price,
            discount=discount,
            category=Category.objects.get(id=category),
            available=available
        )

        for id in images:
            image_item = ImageItem.objects.get(id=id)
            product.images.add(image_item)
        product.save()

        serializer = ProductSerializer(product)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetail (generics.GenericAPIView):
    queryset = Product.objects.all()
    def get(self, request, slug):
        product = Product.objects.filter(slug=slug)
        if product.exists():
            serializer = ProductSerializer(product[0])
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response({'ok': False}, status=status.HTTP_100_CONTINUE)


class CartTotal(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order, created = Order.objects.get_or_create(
            user=request.user, ordered=False)
        return Response({'total': order.get_cart_items}, status=status.HTTP_200_OK)

class CartDetailM(generics.GenericAPIView, mixins.DestroyModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ItemOrderSerializer
    queryset = OrderItem.objects.all()

    def delete(self, request, pk):
        return self.destroy(request, pk)

class CartDetail(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ItemOrderSerializer
    queryset = OrderItem.objects.all()

    def post(self,request):
        id = request.data.get('id')
        quantity = request.data.get('quantity', 0)
        product = Product.objects.get(id=id)
        orderItem = OrderItem.objects.filter(user=request.user, product=product, ordered=False)

        if not orderItem.exists():
            item = OrderItem.objects.create(user=request.user, product=product)
            if(quantity != 0):
                item.quantity = quantity
                item.save()
            serializer = ItemOrderSerializer(item)
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response({'ok':False}, status=status.HTTP_100_CONTINUE)

    def get(self, request):
        items = OrderItem.objects.filter(
            user=request.user, ordered=False)
        if items.exists():
            serializer = OrderItemSerializer(items, many=True)
            return Response({'items':serializer.data}, status=status.HTTP_200_OK)
        return Response({'ok':False}, status=status.HTTP_100_CONTINUE)

    def put(self, request):
        try:
            order_item = OrderItem.objects.get(
                user=request.user,
                id=self.request.data.get('id', 0)
            )

            action = str(self.request.data.get('action', -1))

            if action == '0':
                order_item.quantity += 1
            elif action == '1':
                order_item.quantity -= 1

            order_item.save()
        except ObjectDoesNotExist:
            return Response({'detail': 'No existe el item'}, status=status.HTTP_204_NO_CONTENT)

        return Response({'ok':True},status=status.HTTP_200_OK)

class Wishlist(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistItemSerializer

    def get(self, request):
        items = WishlistItem.objects.filter(user=request.user)
        if items.exists():
            serializer = self.serializer_class(items, many= True)
            if serializer.is_valid:
                return Response({'items':serializer.data}, status=status.HTTP_200_OK)
        return Response({'ok':False}, status=status.HTTP_100_CONTINUE)

    def post(self, request):
        id = request.data.get('id')
        product = Product.objects.get(id=id)
        wishlisItem = WishlistItem.objects.filter(product=product)
        if not wishlisItem.exists():
            item = WishlistItem.objects.create(user=request.user, product=product)
            serializer = ItemOrderSerializer(item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'ok':False}, status=status.HTTP_100_CONTINUE)

class WishlistQ(generics.GenericAPIView, mixins.DestroyModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistItemSerializer
    queryset = WishlistItem.objects.all()
    
    def delete(self, request, pk):
        return self.destroy(request, pk)

class PaymentView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get(self, request):
        json_data = dict()

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            serializer = self.get_serializer(order)
            json_data = {
                'order': serializer.data,
            }
            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                json_data['default_shipping_address'] = shipping_address_qs[0]

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                json_data['default_shipping_address'] = shipping_address_qs[0]
            return Response(json_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'detail': 'No tienes una orden activa'}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        # Fields for Address
        city = request.data.get('city')
        address = request.data.get('address')
        zip = request.data.get('zip')

        # Fields for Payment
        charge_id = request.data.get('charge_id')
        amount = request.data.get('total')

        try:
            location = Address.objects.create(
                user = request.user,
                city = city,
                address = address,
                zip = zip
            )

            payment = Payment.objects.create(
                user = request.user,
                charge_id = charge_id,
                amount = amount,
            )

            order = Order.objects.create(
                user = request.user,
                shipping_address = location,
                payment = payment,
            )

            items = OrderItem.objects.filter(user = request.user, ordered = False)

            for i in items:
                i.ordered = True
                i.save()
                order.products.add(i)
            order.ordered = True
            order.save()

            serializer = OrderSerializer(order)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except:
            return Response({'ok':False}, status=status.HTTP_100_CONTINUE)

""" class PaymentHandler(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order = Order.objects.get(user=request.user, ordered=False)
        data = self.request.data

        order_items = order.products.all()
        order_items.update(ordered=True)
        for item in order_items:
            item.save()

        order.ordered = True
        #order.payment = payment
        order.save()

        Address.objects.create(
            user=request.user,
            order=order,
            address=data.get('address'),
            city=data.get('city'),
            country=data.get('country'),
            zip=data.get('zip'),
            address_type = 'S'
		)

        return Response({'detail':'La factura se ha creado con éxito'}, status=status.HTTP_200_OK) """