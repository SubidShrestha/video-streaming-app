from dataclasses import dataclass
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.conf import settings
from rest_framework import serializers
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken
from .user import UserSerializer

UserModel = get_user_model()

@dataclass
class JWTToken:
    refresh: str
    access: str
    access_token_expiration: datetime
    refresh_token_expiration: datetime

class JWTTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    access_token_expiration = serializers.DateTimeField()
    refresh_token_expiration = serializers.DateTimeField()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, required=True)
    tokens = JWTTokenSerializer(read_only=True)
    
    def validate(self, attrs) -> dict:
        """Validates incoming values and returns authentication params"""
        attrs = super().validate(attrs)
        email = attrs.get('email')
        username = attrs.get('username')
        password = attrs.get('password')
        
        if not (email or username):
            return serializers.ValidationError(_('Email or Username is required'))
        
        if email and password:
            return {'email': email, 'password': password}
        
        if username and password:
            return {'username': username, 'password': password}
    
    def create(self, validated_data):
        """Generates JWT tokens if the user is successfully authenticated else raises AuthenticationFailed exception"""
        self.user = authenticate(**validated_data)

        if not self.user:
            raise exceptions.AuthenticationFailed(_('Authentication failed. Make sure your login info is correct.'))

        if not self.user.is_active:
            raise exceptions.AuthenticationFailed(_('Authentication failed. The user account has been deactivated.'))
        
        update_last_login(None, self.user)

        return {
            'tokens': self.generate_tokens(),
            'user': UserSerializer(self.user).data
        }
    
    def generate_tokens(self):
        refresh_token = RefreshToken.for_user(self.user)
        access_token = refresh_token.access_token
        access_token_expiration = now() + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRATION)
        refresh_token_expiration = now() + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRATION)

        jwt_instance = JWTToken(
            refresh=refresh_token,
            access=access_token,
            access_token_expiration=access_token_expiration,
            refresh_token_expiration=refresh_token_expiration
        )
        
        token_serializer = JWTTokenSerializer(instance = jwt_instance).data
        return token_serializer

    def to_representation(self, instance):
        return instance