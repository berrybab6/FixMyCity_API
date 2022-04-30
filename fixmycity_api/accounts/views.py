from rest_framework import generics, status, permissions, serializers, viewsets
# from rest_framework import serializers
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.gis.geos import GEOSGeometry
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import  InactiveUser, InvalidUser, LoginSerializer, SectorAdminSerializer, SectorSerializer, UserSerializer, LoginSectorAdminSerializer , EmailVerificationSerializer, LoginSectorAdminSerializer , LoginSuperAdminSerializer
from .utils import Utils
from .models import Role, Sector, User
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from permissions import IsSectorAdmin, IsSuperAdmin
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import jwt
from django.conf import settings
from django.http import HttpResponsePermanentRedirect
import os
from django.core.mail import EmailMessage , EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.crypto import get_random_string
from drf_yasg.utils import swagger_auto_schema
from accounts import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.utils import generate_access_token, generate_refresh_token
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from django.contrib.auth.hashers import make_password


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SectorAdminSerializer
     
     
    # @swagger_auto_schema(request_body=LoginSerializer)
    def post(self,request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        email = request.data['email']
        print(user)
        # token = get_random_string(length=32)
        token = RefreshToken.for_user(user).access_token
        verify_link = 'http://localhost:3002' + '/email-verify/' + str( token)
        subject, from_email, to = 'Verify Your Email', 'from@fpn.com', email
        html_content = render_to_string('accounts/verify_email.html', {'verify_link':verify_link, 'base_url': 'http://localhost:3002/', 'backend_url': 'http://127.0.0.1:8000'}) 
        text_content = strip_tags(html_content) 
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # Utils.send_email(data)
        return Response(data=user_data,  status=status.HTTP_201_CREATED)
        
       
        
        

    
class VerifyEmail(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = EmailVerificationSerializer
    @swagger_auto_schema(request_body=EmailVerificationSerializer)
    def post(self, request):
        token = request.data['token']
        print(token)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY , algorithms='HS256')
            print(payload)
            user = User.objects.get(id=payload['user_id'])
            print(user)
            if not user.is_verified:
                user.is_verified = True
                user.password = make_password(request.data['password'])
                user.username = request.data['username']
                user.first_name = request.data['first_name']
                user.last_name = request.data['first_name']
                user.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'status': 'failed'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'status': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    
    
    
    
    
    
    
    
    

class EditProfile(APIView):
    def put(self, request,id):
        user = User.objects.get(id=id)

        data = request.data.dict()

        serializer = UserSerializer(user, data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)




class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny, ]
    # queryset = User.objects.all()
    serializer_class = LoginSerializer
     
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        # username = request.data.get('username' , None)
        # password = request.data.get('password' , None)
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = Utils.authenticate_user(serializer.validated_data)
        # user = authenticate(username = username , password = password)
        print(user)
        # if user:
        #     serializer = self.serializer_class(user)
        #     return Response(serializer.data , status = status.HTTP_200_OK)
        # return Response({"message":"invalid credintials", "status":status.HTTP_401_UNAUTHORIZED})
        # queryset = user
        # serializedUser = UserSerializer(user)
        # token = Utils.encode_token(user)
        access_token = generate_access_token(user)
        print("and this is " ,access_token )
        refresh_token = generate_refresh_token(user)
        
        return Response({"message":"sucess", "token":access_token})
        
    def get_queryset(self):
        return super().get_queryset()
    
class LoginSectorAdminView(APIView):
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()
    serializer_class = LoginSectorAdminSerializer
    def post(self, request):
        serializer = LoginSectorAdminSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = Utils.authenticate_sector_admin(serializer.validated_data)
        # queryset = user
        serializedUser = LoginSectorAdminSerializer(user)
        token = Utils.encode_token(user)
        
        return Response({"data":serializedUser.data, "token":token})
        
    def get_queryset(self):
        return super().get_queryset()
    
    
    
class SectorAPIView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    # permission_classes = ( IsAuthenticated,IsSuperAdmin,)
    # http_method_names = ['get', 'post', 'patch']
    serializer_class = SectorSerializer

    pagination_class = PageNumberPagination
    queryset = Sector.objects.all().order_by("-created_at")
    def get_queryset(self):
        sector = Sector.objects.all().order_by("-created_at")
        return sector
    
    def create(self, request, **kwargs):
        latitude = request.data['lat']
        longtiude = request.data['lng']
        pnt = GEOSGeometry('POINT(%s %s)' % (longtiude, latitude))
        serializer_obj = SectorSerializer(data=request.data)
        
        if serializer_obj.is_valid():
            serializer_obj.save(location=pnt)
            return Response({"message": 'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    

    
  

#     queryset = Sector.objects.all()
#     permission_classes = [AllowAny, ]


#     def get_queryset(self):
#         return super().get_queryset()

    
    
    
    
    def partial_update(self, request, pk=None):
        id = self.kwargs.get("pk")
        try:
            sector = Sector.objects.get(id=id)
            sectorserializer = SectorSerializer(sector, data=request.data, partial=True)
            if sectorserializer.is_valid():
                sectorserializer.save()
                return Response(sectorserializer.data, status=status.HTTP_200_OK)
            return Response(sectorserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Sector.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
        
        
    
    def destroy(self, request, pk=None):
        id = self.kwargs.get("pk")
        try:
            sector = Sector.objects.get(pk=id)
            sector.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except sector.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
        
    
    



    
    
    


class TestView(APIView):
    def get(self, request):
        return Response({"Message":"TEST HOW RESPONSE WORKS"})
    
    
    
    

    
    
class LoginSectorAdmin(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSectorAdminSerializer
    def post(self, request, *args, **kwargs):
        
        req_data = request.data.copy()
        try:
            current_user = User.objects.get(email=req_data['email'])
        except User.DoesNotExist:
            raise AuthenticationFailed('account_doesnt_exist')
        if current_user is not None:
            if not current_user.is_active:
            #raise AuthenticationFailed('account_not_active')
               raise InactiveUser('account_not_active')
            else:
               pass
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(e)
            raise InvalidUser(e.args[0])
        except TokenError as e:
            print(e)
            raise InvalidToken(e.args[0])
        return Response({"message": "Sign In Successfull" , "token":serializer.validated_data }  , status=status.HTTP_200_OK)
        
        
        
        
class LoginSuperAdmin(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSuperAdminSerializer
    def post(self, request, *args, **kwargs):
        req_data = request.data.copy()
        try:
            current_user = User.objects.get(username=req_data['username'])
        except User.DoesNotExist:
            raise AuthenticationFailed('account_doesnt_exist')
        if current_user is not None:
            if not current_user.is_active:
            #raise AuthenticationFailed('account_not_active')
               raise InactiveUser('account_not_active')
            else:
               pass
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(e)
            raise InvalidUser(e.args[0])
        except TokenError as e:
            print(e)
            raise InvalidToken(e.args[0])
        return Response({"message": "Sign In Successfull" , "token":serializer.validated_data }  , status=status.HTTP_200_OK)
        
        