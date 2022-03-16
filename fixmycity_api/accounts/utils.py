from django.contrib.auth import authenticate
from .models import SuperAdmin
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
import django.contrib.auth.password_validation as validators

class Utils:
    @staticmethod
    def encode_token(user):
        payload = {
            'id': user.id,
        }
        token = RefreshToken.for_user(user)
        token.payload['TOKEN_TYPE_CLAIM'] = 'access'

        return {
            'refresh': str(token),
            'access': str(token.access_token),
        }
    @staticmethod
    def authenticate_user(validated_data):
        from .models import User
        username = validated_data['username']
        password = validated_data['password']
        
        user = SuperAdmin.objects.filter(username=username).first()
        if user and authenticate(username = username, password= password):
            return user
            
        
        raise serializers.ValidationError("Invalid username/password. Please try again!")