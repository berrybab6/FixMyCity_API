from django.contrib.auth import authenticate
from .models import User
from users.models import User as users
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
        
        user = User.objects.filter(username=username).first()
        if user and authenticate(username = username, password= password):
            return user
            
        
        raise serializers.ValidationError("Invalid username/password. Please try again!")
    
    
    @staticmethod
    def authenticate_custome_user(validated_data):
        
        phone_number = validated_data['phone_number']
        print(phone_number)
        # password = validated_data['password']
        
        user = users.objects.filter(phone_number=phone_number).first()
        
        if user :
            print(user)
            return user
            
        
        raise serializers.ValidationError("Invalid phone number. Please try again!")