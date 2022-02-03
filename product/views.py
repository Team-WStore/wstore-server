from copy import copy
from numpy import product
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins, generics
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.conf import settings

from .models import Category, Product, Order, Address, OrderItem, WishlistItem
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
    
    def post(self, request):
        name = request.data.get('name')
        price = request.data.get('price')
        category = request.data.get('category')
        discount_price = request.data.get('discount_price')
        images = request.data.get('images', [])

        product = Product.objects.create(
            name=name,
            price=price,
            category=category,
            discount_price=discount_price,
        )

        for id in images:
            image_item = ImageItem.objects.get(id=id)
            product.images.add(image_item)
        product.save()

        serializer = ProductSerializer(product)

        return Response(serializer.data, status=status.HTTP_201_CREATED )


class HandleProductP(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)


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

    def post(self,request):
        id = request.data.get('id')
        product = Product.objects.get(id=id)
        orderItem = OrderItem.objects.filter(product=product)
        if not orderItem.exists():
            OrderItem.objects.create(user=request.user, product=product)
            return Response({'ok':True}, status=status.HTTP_201_CREATED)
        return Response({'ok':False}, status=status.HTTP_100_CONTINUE)

    def get(self, request):
        items = OrderItem.objects.filter(
            user=request.user, ordered=False)
        if items.exists():
            serializer = OrderItemSerializer(items, many=True)
            if serializer.is_valid:
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
            WishlistItem.objects.create(user=request.user, product=product)
            return Response({'ok':True}, status=status.HTTP_201_CREATED)
        return Response({'ok':False}, status=status.HTTP_100_CONTINUE)

class WishlistQ(generics.GenericAPIView, mixins.DestroyModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistItemSerializer
    queryset = WishlistItem.objects.all()
    
    def delete(self, request, pk):
        return self.destroy(request, pk)

class Checkout(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get(self, request):
        json_data = dict()

        try:
            # Api view has to implement even coupon form

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
        try:
            data = self.request.data
            order = Order.objects.get(user=self.request.user, ordered=False)

            use_default_shipping = data.get('use_default_shipping')

            if use_default_shipping:

                address_qs = Address.objects.filter(
                    user=self.request.user,
                    address_type='S',
                    default=True
                )
                if address_qs.exists():
                    shipping_address = address_qs[0]
                    order.shipping_address = shipping_address
                    order.save()
                return Response({'detail': "Dirección de envío por defecto no disponible"}, status=status.HTTP_400_BAD_REQUEST)
                # redirije a checkout
            else:
                # print("User is entering a new shipping address")
                shipping_address1 = data.get('shipping_address')
                shipping_address2 = data.get('shipping_address2')
                shipping_country = data.get('shipping_country')
                shipping_zip = data.get('shipping_zip')

                if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                    shipping_address = Address(
                        user=self.request.user,
                        street_address=shipping_address1,
                        apartment_address=shipping_address2,
                        country=shipping_country,
                        zip=shipping_zip,
                        address_type='S'
                    )
                    shipping_address.save()

                    order.shipping_address = shipping_address
                    order.save()

                    set_default_shipping = data.get('set_default_shipping')
                    if set_default_shipping:
                        shipping_address.default = True
                        shipping_address.save()

                return Response({'detail': 'Por favor llena los campos requeridos para la dirección de envío'}, status=status.HTTP_400_BAD_REQUEST)

            use_default_billing = data.get('use_default_billing')
            same_billing_address = data.get('same_billing_address')

            if same_billing_address:
                billing_address = shipping_address
                billing_address.pk = None
                billing_address.save()
                billing_address.address_type = 'B'
                billing_address.save()
                order.billing_address = billing_address
                order.save()

            elif use_default_billing:
                print("Using the default billing address")
                address_qs = Address.objects.filter(
                    user=self.request.user,
                    address_type='B',
                    default=True
                )
                if address_qs.exists():
                    billing_address = address_qs[0]
                    order.billing_address = billing_address
                    order.save()
                return Response({'detail': "Dirección de envío por defecto no disponible"}, status=status.HTTP_400_BAD_REQUEST)

            else:
                #print("User is entering a new billing address")
                billing_address1 = data.get('billing_address')
                billing_address2 = data.get('billing_address2')
                billing_country = data.get('billing_country')
                billing_zip = data.get('billing_zip')

                if is_valid_form([billing_address1, billing_country, billing_zip]):
                    billing_address = Address(
                        user=self.request.user,
                        street_address=billing_address1,
                        apartment_address=billing_address2,
                        country=billing_country,
                        zip=billing_zip,
                        address_type='B'
                    )
                    billing_address.save()

                    order.billing_address = billing_address
                    order.save()

                    set_default_billing = data.get('set_default_billing')
                    if set_default_billing:
                        billing_address.default = True
                        billing_address.save()

                    return Response({'detail': 'Por favor llena los campos requeridos para la dirección de cartera'}, status=status.HTTP_400_BAD_REQUEST)
                    # El usuario elige qué tipo de pago usar, el frontend lo redirije
            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'detail': 'No tienes una orden activa'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'detail': 'Error: No ingresaste los campos'}, status=status.HTTP_204_NO_CONTENT)

class PaymentHandler(generics.GenericAPIView):
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

        return Response({'detail':'La factura se ha creado con éxito'}, status=status.HTTP_200_OK)