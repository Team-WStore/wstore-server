from rest_framework import generics, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

from .models import ItemCarrousel
from .serializers import ItemCarrouselSerializer

class ItemCarrouselUpdateDelete(
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        mixins.UpdateModelMixin,
        generics.GenericAPIView
    ):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = ItemCarrousel.objects.all()
    serializer_class = ItemCarrouselSerializer
    
    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    def put(self, request, pk):
        return self.update(request, pk)
    
    def delete(self, request, pk):
        return self.destroy(request, pk)

class ItemCarrouselViewSet(
        mixins.ListModelMixin,
        generics.GenericAPIView
    ):
    queryset = ItemCarrousel.objects.all()
    serializer_class = ItemCarrouselSerializer

    def get(self, request):
        return self.list(request)

class ItemCarrouselCreate(
    generics.GenericAPIView,
    mixins.CreateModelMixin
    ):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = ItemCarrousel.objects.all()
    serializer_class = ItemCarrouselSerializer
    
    def post(self, request):
        return self.create(request)