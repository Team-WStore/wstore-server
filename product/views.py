from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import mixins, generics
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from .models import Brand, Category, Payment, Product, Order, Address, OrderItem, WishlistItem
from core.models import ImageItem
from .serializers import BrandSerializer, CategorySerializer, OrderItemSerializer, ProductSerializer, OrderSerializer, ItemOrderSerializer, WishlistItemSerializer

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


class CategoryCreate(
    generics.GenericAPIView,
):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        name = request.data.get('name')
        id = request.data.get('id')
        image = ImageItem.objects.get(id=id)

        category = Category.objects.create(
            name=name,
            image=image,
        )

        serializer = CategorySerializer(category)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryDelete(
    generics.GenericAPIView,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin
):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)


class CategoryUpdate(
    generics.GenericAPIView,
):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def put(self, request):
        name = request.data.get('name')
        category_id = request.data.get('category_id')
        image_id = request.data.get('image_id')

        image = ImageItem.objects.get(id=image_id)
        category = Category.objects.get(id=category_id)

        category.name = name
        category.image = image
        category.save()

        serializer = CategorySerializer(category)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
    mixins.DestroyModelMixin,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    def delete(self, request, pk):
        return self.destroy(request, pk)


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
        description = request.data.get('description')

        product = Product.objects.create(
            name=name,
            brand=Brand.objects.get(id=brand),
            price=price,
            discount=discount,
            category=Category.objects.get(id=category),
            available=available,
            description=description,
        )

        for id in images:
            image_item = ImageItem.objects.get(id=id)
            product.images.add(image_item)
        product.save()

        serializer = ProductSerializer(product)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ItemProductUpdate(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
    def put(self, request):
        id = request.data.get('id')
        name = request.data.get('name')
        brand = request.data.get('brand')
        price = request.data.get('price')
        discount = request.data.get('discount')
        category = request.data.get('category')
        images = request.data.get('images', [])
        available = request.data.get('available')
        description = request.data.get('description')

        product = Product.objects.get(id=id)
        product.images.clear()
        product.name = name
        product.brand = Brand.objects.get(id=brand)
        product.price = price
        product.discount = discount
        product.category = Category.objects.get(id=category)
        product.available = available
        product.description = description

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
        return Response({'ok': False}, status=status.HTTP_204_NO_CONTENT)


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

    def post(self, request):
        id = request.data.get('id')
        quantity = request.data.get('quantity', 0)
        product = Product.objects.get(id=id)
        orderItem = OrderItem.objects.filter(
            user=request.user, product=product, ordered=False)

        if not orderItem.exists():
            item = OrderItem.objects.create(user=request.user, product=product)
            if(quantity != 0):
                item.quantity = quantity
                item.save()
            serializer = ItemOrderSerializer(item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'ok': False}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request):
        items = OrderItem.objects.filter(
            user=request.user, ordered=False)
        if items.exists():
            serializer = OrderItemSerializer(items, many=True)
            return Response({'items': serializer.data}, status=status.HTTP_200_OK)
        return Response({'ok': False}, status=status.HTTP_204_NO_CONTENT)

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

        return Response({'ok': True}, status=status.HTTP_200_OK)


class Wishlist(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistItemSerializer

    def get(self, request):
        items = WishlistItem.objects.filter(user=request.user)
        if items.exists():
            serializer = self.serializer_class(items, many=True)
            if serializer.is_valid:
                return Response({'items': serializer.data}, status=status.HTTP_200_OK)
        return Response({'ok': False}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        id = request.data.get('id')
        product = Product.objects.get(id=id)
        wishlisItem = WishlistItem.objects.filter(product=product)
        if not wishlisItem.exists():
            item = WishlistItem.objects.create(
                user=request.user, product=product)
            serializer = ItemOrderSerializer(item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'ok': False}, status=status.HTTP_204_NO_CONTENT)


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

        
        location = Address.objects.create(
                user=request.user,
                city=city,
                address=address,
                zip=zip
            )

        payment = Payment.objects.create(
                user=request.user,
                charge_id=charge_id,
                amount=amount,
            )

        order = Order.objects.create(
                user=request.user,
                shipping_address=location,
                payment=payment,
            )

        items = OrderItem.objects.filter(user=request.user, ordered=False)

        for i in items:
            i.ordered = True
            i.save()
            order.products.add(i)
            
        order.ordered = True
        order.save()

        order.total = order.get_total
        order.save()

        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BrandView(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class BrandUpdateDelete(
    generics.GenericAPIView,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin
):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

# Clase para visualizar todas las facturas desde Admin
class OrderView(
    generics.GenericAPIView,
    mixins.ListModelMixin
):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request):
        return self.list(request)
    
    def put(self, request):
        reviewed = request.data.get('reviewed', False)
        sent = request.data.get('sent', False)
        delivered = request.data.get('delivered', False)

        id = request.data.get('id')
        order = Order.objects.get(id=id)

        if reviewed:
            order.reviewed = True
            order.reviewed_date = timezone.now()
        
        if sent:
            order.sent = True
            order.sent_date = timezone.now()
        
        if delivered:
            order.delivered = True
            order.delivered_date = timezone.now()
        
        order.save()

        return Response({'ok':True}, status=status.HTTP_200_OK)

class OrderRetrieve(generics.GenericAPIView, mixins.RetrieveModelMixin):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)
    
# Vista para ser usada para ver las facturas desde un usuario corriente
class OrderDetail(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        orders = Order.objects.filter(user=request.user)

        if orders.exists():
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_204_NO_CONTENT)

class SearchFilter(generics.GenericAPIView):

    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def post(self, request):
        phrase = request.data.get('phrase', '')

        products = Product.objects.filter(name__icontains=phrase)
        if products.exists():
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_204_NO_CONTENT)