from numpy import percentile
from rest_framework import generics, status, permissions, serializers, viewsets
# from rest_framework import serializers
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.gis.geos import GEOSGeometry
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import  InactiveUser, InvalidUser, ResetPasswordEmailRequestSerializer,RoleSerializer, LoginSerializer, SectorAdminSerializer, SectorSerializer, SetNewPasswordSerializer, UserSerializer, LoginSectorAdminSerializer , EmailVerificationSerializer, LoginSectorAdminSerializer , LoginSuperAdminSerializer, ChangePasswordSerializer
from .utils import Utils
from .models import Role, Sector, User
from .utils import Utils
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
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse, reverse_lazy


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


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
                # user.username = request.data['username']
                user.first_name = request.data['first_name']
                user.last_name = request.data['first_name']
                user.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'status': 'failed'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'status': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SectorAdminSerializer
     
     
    # @swagger_auto_schema(request_body=LoginSerializer)
    def post(self,request):
        user = request.data
        sector = request.data.get('sector', False)
        email = request.data['email']
        print("sector is", sector)
        
        if(sector and email):
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_data = serializer.data
        
        user = User.objects.get(email=user_data['email'])
        
        print(user)
        # token = get_random_string(length=32)
        token = RefreshToken.for_user(user).access_token
        verify_link = 'http://localhost:3000' + '/register/?' +'token='+ str( token)
        subject, from_email, to = 'Verify Your Email', 'from@fpn.com', email
        html_content = render_to_string('accounts/verify_email.html', {'verify_link':verify_link, 'base_url': 'http://localhost:3000/', 'backend_url': 'http://127.0.0.1:8000'}) 
        text_content = strip_tags(html_content) 
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # Utils.send_email(data)
        return Response({"Detail": "succesfully registerd!"},  status=status.HTTP_201_CREATED)

########################  DASHBOARD #####################

from .models import User as u
# from users.serializers import RegistorUserSerializer as customU

class UserCount(APIView):
    permission_classes = [AllowAny,]
    queryset = [u.objects.all()]
    # serializer_classes = [SectorAdminSerializer, customU]
    def get(self, request):
        role_s = Role.objects.get(id=2)
        role_u = Role.objects.get(id=3)

        sectors = u.objects.filter(roles=role_s).count()
        users = u.objects.filter(roles=role_u).count()
        banned = u.objects.filter(roles=role_u,active=False).count()
              
        return Response({"sectors":[sectors, "Sectors"], "users":[users, "Custom Users"], "banned":[banned,"Banned Users"]})
        
    def get_queryset(self):
        return super().get_queryset()
    
class SectorCount(APIView):
    permission_classes = [AllowAny,]
    queryset = [Sector.objects.all()]
    # serializer_classes = [SectorAdminSerializer, customU]
    def get(self, request):
        water = Sector.objects.filter(sector_type=2).count()
        tele = Sector.objects.filter(sector_type=1).count()
        elpa = Sector.objects.filter(sector_type=4).count()
        roads = Sector.objects.filter(sector_type=3).count()

        return Response({"tele":[tele, "Tele"], "water":[water, "Water And Sewage"], "roads":[roads,"Roads"], "elpa":[elpa, "ELPA"]})
      
    def get_queryset(self):
        return super().get_queryset()

    
class RoleView(generics.GenericAPIView):
    
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    permission_classes = [AllowAny, ]

    def post(self,request):

        ad = Role.objects.get_or_create(id=1)
        ser1 = RoleSerializer(ad)

        sec = Role.objects.get_or_create(id=2)
        ser2 = RoleSerializer(sec)
    
        custom = Role.objects.get_or_create(id=3)
        ser3 = RoleSerializer(custom)
        
        counts = Role.objects.count()
        if counts>=3:
            roles = Role.objects.all()
            ser = RoleSerializer(roles,many=True)
            return JsonResponse({"Roles":ser.data,"message":"All Roles are already created"})
        else: 
            return JsonResponse({"role1":ser1.data,"role2":ser2.data,"role3":ser3.data,"count":counts}) 



class ActiveSectorCount(APIView):
    permission_classes = [AllowAny,]
    queryset = [User.objects.all()]
    serializer_class = [SectorAdminSerializer]
    def percentage(self, part, whole):
        perc = 0
        if(whole > 0):
            perc = 100 * float(part)/float(whole)
        return int(perc)
    def get(self, request):
         
        valCount = []
        percCount = []
        
        names = ["Telecommunication", "Water And Sewage", "Roads Authority", "ELPA"]
        val3 = []
        ########## Count Active Water Sector Admins
        for i in range(0, 4):
            waters = Sector.objects.filter(sector_type = i+1)

            # vals.append(waters)

            for water in waters:
                role = Role.objects.get(id=2)
                water_count = User.objects.filter(roles=role,active = True, sector=water).count()
                t_sectors = User.objects.filter(roles=role,sector=water).count()
                valCount.append(water_count)
                water_perc = self.percentage(water_count, t_sectors)
                percCount.append(water_perc)
            val3.append([valCount[i], percCount[i],names[i]])
        return Response(val3)
        # return Response({"waterSectors":[water_count, water_perc], "teleCount":tele_count, "roadCount":road_count, "elpaCount":[elpa_count, elpa_perc]})
      
    def get_queryset(self):
        return super().get_queryset()
########################  DASHBOARD #####################



    
    
    
    
    
    
    
    
    

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
    
   
class MainSectorAPIView(APIView):
    permission_classes = [AllowAny, ]
    queryset = Sector.objects.filter(main_sector = True)
    serializer_class = SectorSerializer
   
    
    def get_queryset(self):
        return super().get_queryset()
    def get(self, request):
        s = Sector.objects.filter(main_sector = True)
        if s:
            ser = SectorSerializer(s, many=True)
            return JsonResponse({"sectors":ser.data})
        else:
            return JsonResponse({"error":"No data"})


class UserView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def get(self, request):
        users = User.objects.all()
        if users:
            ser = UserSerializer(users, many=True)
            return JsonResponse({"user":ser.data})
        else:
            JsonResponse({"error":"NO User Found","user":[]})
class UserDetailView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def get(self, request, pk=None):
        user = User.objects.get(id = pk)
        if user:
            ser = UserSerializer(user)
            return JsonResponse({"user":ser.data})
        else:
            JsonResponse({"error":"NO User Found"})

class CustomUserAPIView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    # permission_classes = ( IsAuthenticated,IsSuperAdmin,)
    # http_method_names = ['get', 'post', 'patch']
    serializer_class = UserSerializer

    pagination_class = PageNumberPagination
    # queryset = Sector.objects.all().order_by("-created_at")
    queryset = User.objects.all()

    def get_queryset(self):
        role = Role.objects.get(id=3)
        user = User.objects.filter(roles=role)
        return user
    def get(self, request):
        role = Role.objects.get(id=3)
        users = User.objects.filter(roles=role,active = True)
        if users:
            ser = User(users, many=True)
            return JsonResponse({"users":ser.data})
        else :
            return JsonResponse({"users":[]})

# class BanCustomUserAPIView(generics.GenericAPIView):
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = User

#     pagination_class = PageNumberPagination
#     queryset = User.objects.all()
    
#     def get_queryset(self):
#         role = Role.objects.get(id=3)
#         user = User.objects.filter(roles=role)
#         return user
    
#     def put(self, request, pk=None):
#         try:
#             role = Role.objects.get(id=3)
#             user = User.objects.get(id=pk,roles=role)
#             if user:
#                 user.active = False
#                 user.save()
#                 return Response({"message":"User is Banned"}, status=status.HTTP_200_OK)
#             return Response({"errors":"an error occured"}, status=status.HTTP_400_BAD_REQUEST)
#         except Sector.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
class SectorAPIView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    # permission_classes = ( IsAuthenticated,IsSuperAdmin,)
    # http_method_names = ['get', 'post', 'patch']
    serializer_class = SectorSerializer

    pagination_class = PageNumberPagination
    # queryset = Sector.objects.all().order_by("-created_at")
    queryset = Sector.objects.all().order_by("-sector_type")

    def get_queryset(self):
        sector = Sector.objects.all().order_by("-sector_type")
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
    
    
    
    


class RequestPasswordResetEmail(generics.GenericAPIView):
    permission_classes = [AllowAny, ]
    success_url=reverse_lazy('accounts:password-reset')
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            print(current_site)
            # verify_link = 'http://localhost:3002' + '/email-verify/' + str( token)
            relativeLink = reverse(
                'accounts:password-reset', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink 
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Utils.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny, ]

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)



class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny, ]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
    
    
    

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"Detail": "old password is wrong."}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'Detail': 'Password updated successfully',
                
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        




