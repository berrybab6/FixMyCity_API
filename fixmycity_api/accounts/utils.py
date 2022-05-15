import email
from django.contrib.auth import authenticate
from .models import  User 
# from users.models import User as users
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.core.mail import EmailMessage
from rest_framework.response import Response


import threading
# accounts.utils
import datetime
import jwt
from django.conf import settings


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

class Utils:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()
    
    
    
    
    @staticmethod
    def encode_token(user):
        payload = {
            'id': user.id,
            'role':user.roles
        }
        token = RefreshToken.for_user(user)
        print("this is inside utils" , token)
        token.payload['TOKEN_TYPE_CLAIM'] = 'access'

        return {
            'refresh': str(token),
            'access': str(token.access_token),
        }
    @staticmethod
    def authenticate_user(validated_data):
        from .models import User
        email = validated_data['email']
        password = validated_data['password']
        
        user = User.objects.filter(email=email).first()
        if user and authenticate(email = email, password= password):
            return user
            
        
        return Response({"message":"invalid email or password"})
    
    
    
    
    
    @staticmethod
    def authenticate_sector_admin(validated_data):
        # from .models import User
        email = validated_data['email']
        password = validated_data['password']
        
        user = User.objects.filter(email=email).first()
        if user  and authenticate(email = email, password= password):
            return user
            
        
        raise serializers.ValidationError("Invalid email/password. Please try again!")
    
    
    
    
    
    
    @staticmethod
    def authenticate_custome_user(validated_data):
        
        phone_number = validated_data['phone_number']
        print(phone_number)
        # password = validated_data['password']
        
        user = User.objects.filter(phone_number=phone_number).first()
        
        if user :
            print(user)
            return user
            
        
        raise serializers.ValidationError("Invalid phone number. Please try again!")
    
    
    
    



def generate_access_token(user):

    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm='HS256').decode('utf-8')

    return refresh_token