from numpy import percentile
from rest_framework import generics, status, permissions, serializers, viewsets
# from rest_framework import serializers
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.gis.geos import GEOSGeometry
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import CustomUserSerializer, LoginSerializer, SectorAdminSerializer, SectorSerializer, UserSerializer, LoginSectorAdminSerializer
from .serializers import LoginSerializer, RoleSerializer, SectorAdminSerializer, SectorSerializer, UserSerializer
from .utils import Utils
from .models import CustomUser, Role, Sector, User,SectorAdmin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from permissions import IsSectorAdmin, IsSuperAdmin


########################  DASHBOARD #####################

from .models import CustomUser as u
# from users.serializers import RegistorUserSerializer as customU

class UserCount(APIView):
    permission_classes = [AllowAny,]
    queryset = [u.objects.all(), SectorAdmin.objects.all()]
    # serializer_classes = [SectorAdminSerializer, customU]
    def get(self, request):
        
        sectors = SectorAdmin.objects.count()
        users = u.objects.count()
        banned = u.objects.filter(active=False).count()
              
        return Response({"sectors":[sectors, "Sectors"], "users":[users, "Custom Users"], "banned":[banned,"Banned Users"]})
        
    def get_queryset(self):
        return super().get_queryset()
    
class SectorCount(APIView):
    permission_classes = [AllowAny,]
    queryset = [Sector.objects.all()]
    def get(self, request):
        
        water = Sector.objects.filter(sector_type=2).count()
        tele = Sector.objects.filter(sector_type=1).count()
        elpa = Sector.objects.filter(sector_type=4).count()
        roads = Sector.objects.filter(sector_type=3).count()


              
        return Response({"tele":[tele, "Tele"], "water":[water, "Water And Sewage"], "roads":[roads,"Roads"], "elpa":[elpa, "ELPA"]})
      
    def get_queryset(self):
        return super().get_queryset()


class ActiveSectorCount(APIView):
    permission_classes = [AllowAny,]
    queryset = [SectorAdmin.objects.all()]
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
                
                water_count = SectorAdmin.objects.filter(active = True, sector=water).count()
                t_sectors = SectorAdmin.objects.filter(sector=water).count()
                valCount.append(water_count)
                water_perc = self.percentage(water_count, t_sectors)
                percCount.append(water_perc)
            val3.append([valCount[i], percCount[i],names[i]])
        return Response(val3)
        # return Response({"waterSectors":[water_count, water_perc], "teleCount":tele_count, "roadCount":road_count, "elpaCount":[elpa_count, elpa_perc]})
      
    def get_queryset(self):
        return super().get_queryset()
########################  DASHBOARD #####################


class RegisterView(APIView):
    permission_classes = [IsAdminUser, ]
    serializer_class = [SectorAdminSerializer]
    def post(self,request):
        data = request.data
        username_ = data['username']
        password_ = data['password']
        email_ = data['email']
        full_name_ = data['full_name']
        sector_= data['sector']
        sec= Sector.objects.get(id=sector_)
        role = Role.objects.get(id=2)
        user = SectorAdmin(username=username_,password=password_,email=email_, full_name=full_name_, roles=role,main_sector=True,sector=sec)
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
    serializer_class = CustomUserSerializer

    pagination_class = PageNumberPagination
    # queryset = Sector.objects.all().order_by("-created_at")
    queryset = CustomUser.objects.all()

    def get_queryset(self):
        user = CustomUser.objects.all()
        return user
    def get(self, request):
        users = CustomUser.objects.filter(active = True)
        if users:
            ser = CustomUserSerializer(users, many=True)
            return JsonResponse({"users":ser.data})
        else :
            return JsonResponse({"users":[]})

class BanCustomUserAPIView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer

    pagination_class = PageNumberPagination
    queryset = CustomUser.objects.all()
    
    def get_queryset(self):
        user = CustomUser.objects.all()
        return user
    
    def put(self, request, pk=None):
        try:
            user = CustomUser.objects.get(id=pk)
            if user:
                user.active = False
                user.save()
                return Response({"message":"User is Banned"}, status=status.HTTP_200_OK)
            return Response({"errors":"an error occured"}, status=status.HTTP_400_BAD_REQUEST)
        except Sector.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
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
    
    
    
    

    
    # def list(self, request, *args, **kwargs):
    #     report = Sector.objects.all().order_by("-created_at")
    #     serializer = SectorSerializer(report , many= True)
    #     qs = super().get_queryset()
      
    #     latitude = self.request.query_params.get('lat', None)
    #     longtiude = self.request.query_params.get('lng', None)
    #     if latitude and longtiude:
    #         pnt = GEOSGeometry('POINT(%s %s)' % (longtiude, latitude) , srid=4326)
    #         qs = qs.annotate(distance= Distance('location' , pnt)).filter(distance__lte=3000).order_by("-postedAt")
    #         serializer = ReportSerializer(qs , many= True)
    #     return Response(serializer.data)

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
        
        
        
    # def get_permissions(self):
    #     """Set custom permissions for each action."""
    #     if self.action in [ 'partial_update', 'destroy', ]:
    #         self.permission_classes = [IsAuthenticated, IsSuperAdmin]
    #     elif self.action in ['list' ,]:
    #         self.permission_classes = [IsAuthenticated  ]
    #     elif self.action in ['create']:
    #         self.permission_classes = [IsAuthenticated , IsSuperAdmin ]
    #     return super().get_permissions()
    
    



    
    
    
# class SectorView(viewsets.ModelViewSet):
    
#     serializer_class = SectorSerializer
#     queryset = Sector.objects.all()
#     permission_classes = [IsAdminUser, ]


#     def get_queryset(self):
#         return super().get_queryset()
    


# class SectorAPIView(viewsets.ModelViewSet):
#     # permission_classes = (IsAuthenticated,IsSectorAdmin )
#     serializer_class = SectorSerializer
   
#     queryset = Sector.objects.all().order_by("-created_at")
#     def get_queryset(self):
#         report = Sector.objects.all().order_by("-created_at")
#         return report
    
#     def create(self, request, **kwargs):
#         address = request.data['address']
#         print("address is" , address)
#         g = geocoder.google(address)
#         print("after geo coder is ", g)
#         latitude = g.latlng[0]
#         longtiude = g.latlng[1]
#         pnt = GEOSGeometry('POINT(%s %s)' % (longtiude, latitude))
#         serializer_obj = SectorSerializer(data=request.data)
        
#         if serializer_obj.is_valid():
#             serializer_obj.save(location=pnt)
#             return Response({"msg": 'Data Created'}, status=status.HTTP_201_CREATED)
#         return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
   
    
    
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

        

        
    

class TestView(APIView):
    def get(self, request):
        return Response({"Message":"TEST HOW RESPONSE WORKS"})