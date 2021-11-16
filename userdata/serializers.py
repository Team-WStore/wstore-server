from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'name',
            'lastname',
            'phone',
            'identity',
            'address',
            'avatar'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ChangeEmailSerializer(serializers.Serializer):
    model = User

    email = serializers.EmailField(required=True)
