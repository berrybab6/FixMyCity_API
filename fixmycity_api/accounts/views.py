
from django.shortcuts import render
from rest_framework import generics, status, permissions, serializers, viewsets

# from rest_framework import serializers
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.http import JsonResponse
<<<<<<< HEAD
from .serializers import LoginSerializer, SectorAdminSerializer, SectorSerializer, UserSerializer, LoginSectorAdminSerializer
=======
from .serializers import LoginSerializer, RoleSerializer, SectorAdminSerializer, SectorSerializer, UserSerializer
>>>>>>> db4b4432df78eec5426ec1963c5f20c2a5cc687b
from .utils import Utils
from .models import Role, Sector, User,SectorAdmin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

# Create your views here.


class RegisterView(APIView):
    permission_classes = [IsAdminUser, ]
    serializer_class = [SectorAdminSerializer]
    def post(self,request):
        data = request.data
        username_ = data['username']
        password_ = data['password']
        email_ = data['email']
        full_name_ = data['full_name']
        role = Role.objects.get(id=2)
        user = SectorAdmin(username=username_,password=password_,email=email_, full_name=full_name_, roles=role,main_sector=True )
        user.save()
        serializer = SectorAdminSerializer(user)

        return Response({"data":serializer.data})

class EditProfile(APIView):
    def put(self, request,id):
        user = User.objects.get(id=id)

        data = request.data.dict()

        serializer = UserSerializer(user, data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)




class LoginView(APIView):
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = Utils.authenticate_user(serializer.validated_data)
        # queryset = user
        serializedUser = UserSerializer(user)
        token = Utils.encode_token(user)
        
        return Response({"data":serializedUser.data, "token":token})
        
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
        serializedUser = SectorAdminSerializer(user)
        token = Utils.encode_token(user)
        
        return Response({"data":serializedUser.data, "token":token})
        
    def get_queryset(self):
        return super().get_queryset()
    
    
    
class SectorView(viewsets.ModelViewSet):
    
    serializer_class = SectorSerializer
    queryset = Sector.objects.all()
    permission_classes = [IsAdminUser, ]


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
        

    def get_queryset(self):
        return super().get_queryset()

class TestView(APIView):
    def get(self, request):
        return Response({"Message":"TEST HOW RESPONSE WORKS"})