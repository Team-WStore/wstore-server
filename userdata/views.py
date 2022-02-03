from rest_framework import generics, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from copy import copy

# Model and Serializer
from .models import Profile
from .serializers import ProfileSerializer, ChangePasswordSerializer, ChangeEmailSerializer

# Create your views here.
class HandleProfile(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    class_parser = (FileUploadParser, MultiPartParser, JSONParser, )
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get(self, request):
        profile = get_object_or_404(
            Profile,
            user=request.user
        )

        serializer = ProfileSerializer(profile)
        data_profile = copy(serializer.data)
        data_profile['email'] = profile.user.email
        return Response(data_profile)

    def put(self, request):

        profile = get_object_or_404(
            Profile,
            user=self.request.user
        )

        if(self.request.data.get('action') == 'delete'):
            profile.avatar.delete()  # To delete Image from DIR media
            profile.save()

        dataSerializer = ProfileSerializer(
            profile,
            data=request.data
        )

        if dataSerializer.is_valid():
            dataSerializer.save()
            return Response(dataSerializer.data, status=200)
        else:
            return Response(dataSerializer.errors, status=400)


class ChangePasswordView(generics.UpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=400)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'OK'
            }

            return Response(response)

        return Response(serializer.errors, status=400)


class ChangeEmailView(generics.UpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ChangeEmailSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check email
            if User.objects.filter(email=serializer.data.get("email")).exists():
                return Response({"email": ["El email ya existe, no se puede usar."]}, status=400)
            # set_email into object type user

            self.object.email = serializer.data.get("email")
            self.object.save()
            response = {
                'status': 'OK'
            }

            return Response(response)

        return Response(serializer.errors, status=400)
