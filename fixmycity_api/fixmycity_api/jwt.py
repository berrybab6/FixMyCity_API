import re
from rest_framework.authentication import get_authorization_header ,  BaseAuthentication
from rest_framework import exceptions
import jwt
from django.conf import settings

# from accounts.models import User 

# from accounts.models import User
# from accounts.models import  User 

class JwtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        auth_data = auth_header.decode('utf-8')
        auth_token = auth_data.split(" ")
        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed("token not valid")
        token = auth_token[1]
        try:
            payload = jwt.decode(token , settings.SECRET_KEY , algorithms='HS256')
            username = payload['username']
            user = settings.AUTH_USER_MODEL.objects.get(username= username)
            return (user , token )
        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed("token is expired")
        
        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed("token is invalid")
        
        except settings.AUTH_USER_MODEL.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed("no such user")
            
         
        return super().authenticate(request)