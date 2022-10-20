from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist

from author.serializers import AuthorSerializer
from author.models import Author


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['user'] = AuthorSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class RegisterSerializer(AuthorSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
    displayName = serializers.CharField(max_length=200, required=True, write_only=True)

    class Meta:
        model = Author
        fields = ['id', 'displayName', 'github', 'password', 'host']

    def create(self, validated_data):
        try:
            user = Author.objects.get(displayName=validated_data['displayName'])
        except ObjectDoesNotExist:
            user = Author.objects.create_user(**validated_data)
        return user