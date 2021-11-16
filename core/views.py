from rest_framework import generics, mixins

from .models import ItemCarrousel
from .serializers import ItemCarrouselSerializer

class ItemCarrouselUpdateDelete(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        mixins.UpdateModelMixin,
        generics.GenericAPIView
    ):
    queryset = ItemCarrousel.objects.all()
    serializer_class = ItemCarrouselSerializer
    
    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    def post(self, request):
        return self.create(request)
    
    def put(self, request, pk):
        return self.update(request, pk)
    
    def delete(self, request, pk):
        return self.destroy(request, pk)

class ItemCarrouselViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        mixins.UpdateModelMixin,
        generics.GenericAPIView
    ):
    queryset = ItemCarrousel.objects.all()
    serializer_class = ItemCarrouselSerializer

    def get(self, request):
        return self.list(request)