
from urllib import response
from django.forms import CharField, ValidationError
from numpy import full
from requests import Response
from rest_framework import serializers, fields

from .models import Sector, User , Role
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import PasswordField
from django.contrib.auth import authenticate


from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken , TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']
        
        
        
        
        
        
        
    
class SectorAdminSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(
    #     max_length=68, min_length=6, write_only=True)

    # default_error_messages = {
    #     'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ['email' , 'roles' , 'sector']
        
    def create(self, validated_data):
        role = Role.objects.get(id=2)
        user = User(email= validated_data['email'],roles = role , sector = validated_data['sector'] )
        user.save()
        return user

    # def validate(self, attrs):
    #     email = attrs.get('email' )
    #     raise serializers.ValidationError(
    #     self.default_error_messages)
        # username = attrs.get('username', '')

        # if not username.isalnum():
        #     raise serializers.ValidationError(
        #         self.default_error_messages)
        # return attrs

    # def create(self, validated_data):
    #     return User.objects.create_user(**validated_data)

   
    
    
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']
    
    
    
    
    
    
    
    
    

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['username' , 'password',]
    

class LoginSectorAdminSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.CharField(required=True)

    # def create(self, validated_data):
        # return User.objects.create(**validated_data)
# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = "__all__"
#         # extra_kwargs = {'password': {'write_only': True}}
#         read_only_fields = ['id']  
class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = "__all__"
        # extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']    
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = ['id']    
        
        
        
        

    
class InvalidUser(AuthenticationFailed):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = ("Credentials is invalid or didn't match")
    default_code = 'user_credentials_not_valid'
    
    
class InactiveUser(AuthenticationFailed):
     status_code = status.HTTP_406_NOT_ACCEPTABLE
     default_detail = ("Credentials is invalid or didn't match")
     default_code = 'user_inactive'
    
class LoginSectorAdminSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD
    @classmethod
    def get_token(cls, user):
          token = super(LoginSectorAdminSerializer, cls).get_token(user)

          # Add custom claims
          token['sector']  = user.sector.district_name
          token['email'] = user.email
          token['role'] = user.role
          return token
        

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
    
    
    
    

class LoginSuperAdminSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
          token = super(LoginSuperAdminSerializer, cls).get_token(user)

          # Add custom claims
          token['username'] = user.username
          token['role'] = user.role
          return token
        

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
    
    
    
    
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)



class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)