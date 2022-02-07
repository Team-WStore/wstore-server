from rest_framework import generics, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ItemCarrousel
from .serializers import ItemCarrouselSerializer

class ItemCarrouselUpdateDelete(
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        mixins.UpdateModelMixin,
        generics.GenericAPIView
    ):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ItemCarrousel.objects.all()
    serializer_class = ItemCarrouselSerializer
    
    def get(self, request, pk):
        if request.user.is_staff:
            return self.retrieve(request, pk)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request, pk):
        if request.user.is_staff:
            return self.update(request, pk)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, pk):
        if request.user.is_staff:
            return self.destroy(request, pk)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

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
    permission_classes = [IsAuthenticated]
    queryset = ItemCarrousel.objects.all()
    serializer_class = ItemCarrouselSerializer
    
    def post(self, request):
        if request.user.is_staff:
            return self.create(request)
        return Response(status=status.HTTP_401_UNAUTHORIZED)