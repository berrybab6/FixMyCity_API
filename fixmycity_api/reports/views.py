from dis import dis
import re
from tracemalloc import start

from turtle import distance
from rest_framework.views import APIView
from .models import F, Report
from .serializers import LocationSerializer, ReportSerializer ,ReportUpdateSerializer, MyReportUpdateSerializer


from django.http import JsonResponse
from accounts.models import Role, Sector, User
from accounts.serializers import SectorAdminSerializer, SectorSerializer


# from .serializers import LocationSerializer, ReportSerializer ,ReportUpdateSerializer


from rest_framework import status , filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from permissions import IsSectorAdmin , IsCustomUser, IsSuperAdmin
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from .apps import ReportsConfig
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend





class ReportAPIView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    # authentication_classes = []
    # permission_classes = (IsAuthenticated,IsSectorAdmin )
    
    http_method_names = ['get', 'post', 'patch' , 'delete' ]
    serializer_class = ReportSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('id' , 'state' , 'status' , 'spamStatus',)
    search_fields = ('tag' , 'description' , 'user__first_name', 'user__last_name', 'sector__district_name' , 'user__phone_number')
    queryset = Report.objects.all().order_by("-postedAt")
    def get_queryset(self):
        report = Report.objects.all().order_by("-postedAt")
        return report
    
    @action(detail=False)
    def getreportbasedonSectorName(self , request):
        sector_name=self.request.user.sector
        print(sector_name)
        report = Report.objects.filter(sector__district_name=sector_name).order_by("-postedAt")
        # serializer = ReportSerializer(report , many= True)
        serializer = ReportSerializer(self.filter_queryset(self.get_queryset()), many=True,)
        return Response(serializer.data)
    
    
    @action(detail=False)
    def getreportbasedonSectorNameandLocation(self , request):
        sector_name=self.request.user.sector
        sector_location = self.request.user.sector.location
        print(sector_location)
        qs = super().get_queryset()
        pnt = sector_location
        qs = qs.annotate(distance= Distance('location' , pnt)).filter(distance__lte=3000 ,sector__district_name=sector_name ).order_by("-postedAt")
        serializer = ReportSerializer(self.filter_queryset(self.get_queryset()), many=True,)
        # serializer = ReportSerializer(qs , many= True)
        return Response(serializer.data)
    
    
    
    
    
        
    
    def create(self, request, **kwargs):
        latitude = request.data['latitude']
        longtiude = request.data['longtiude']
        pnt = GEOSGeometry('POINT(%s %s)' % (longtiude, latitude))
        serializer_obj = ReportSerializer(data=request.data)
        image = request.data['image']
        # lin_reg_model = ReportsConfig.model
        # image_predicted = lin_reg_model.predict(image)
        image_predicted = 0
        if image_predicted == 1:
            serializer_obj = ReportSerializer(data=request.data)
            if serializer_obj.is_valid():
                serializer_obj.save(location=pnt , spamStatus=True)
                return Response({"detail": 'Data Created'}, status=status.HTTP_201_CREATED)
            return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer_obj = ReportSerializer(data=request.data , )
            if serializer_obj.is_valid():
                serializer_obj.save(location=pnt , spamStatus=False)
                return Response({"detail": 'Data Created'}, status=status.HTTP_201_CREATED)
            return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
            
    
    
    
    

    
    def list(self, request, *args, **kwargs):
        report = Report.objects.all().order_by("-postedAt")
        # serializer = ReportSerializer(report , many= True)
        serializer = ReportSerializer(self.filter_queryset(self.get_queryset()), many=True,)
        
        qs = super().get_queryset()
      
        latitude = self.request.query_params.get('lat', None)
        longtiude = self.request.query_params.get('lng', None)
        if latitude and longtiude:
            pnt = GEOSGeometry('POINT(%s %s)' % (longtiude, latitude) , srid=4326)
            distance = Distance('location' , pnt)
            qs = qs.annotate(distance= Distance('location' , pnt)).filter(distance__lte=3000).order_by("-postedAt")
            serializer = ReportSerializer(qs , many= True)
        return Response(serializer.data)
        

    
    
    
    
    
    def partial_update(self, request, pk=None):
        id = self.kwargs.get("pk")
        try:
            
            # print(self.request.user.sector)
            #  announcment = Announcement.objects.filter(sectoradmin__sector_user=self.request.user).get(id=id)
            # report = Report.objects.filter(sector__district_name=self.request.user.sector).get(id=id)
            report = Report.objects.get(id=id)

            reportserializer = ReportUpdateSerializer(report, data=request.data, partial=True)
            if reportserializer.is_valid():
                reportserializer.save()
                serializer = ReportSerializer(report)

                return Response({"detail" : "Report updated successfully!", "report":serializer.data}, status=status.HTTP_200_OK)
            return Response(reportserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Report.DoesNotExist:
            return Response({"detail" : 'Report does not exist or you dont have permission to update it'} , status=status.HTTP_404_NOT_FOUND)
        
        
        
        
    
    def destroy(self, request, pk=None):
        print("i am here actually")
        
        id = self.kwargs.get("pk")
        try:
            report = Report.objects.filter(sector__district_name=self.request.user.sector).get(id=id)
            print(report)
            # report = Report.objects.get(pk=id)
            report.delete()
            return Response( {"detail" : "report deleted succesfully!"} , status=status.HTTP_204_NO_CONTENT)
        except Report.DoesNotExist:
            return Response({"detail": "Report doest not exist or you dont have permission to delete it"} , status=status.HTTP_404_NOT_FOUND)
        
        
        
    # def get_permissions(self):
    #     """Set custom permissions for each action."""
    #     if self.action in [ 'partial_update', 'destroy', 'getreportbasedonSectorName' , 'getreportbasedonSectorNameandLocation']:
    #         self.permission_classes = [IsAuthenticated, IsSectorAdmin]
    #     elif self.action in ['list' , 'retrieve']:
    #         self.permission_classes = [IsAuthenticated  ]
    #     elif self.action in ['create']:
    #         self.permission_classes = [IsAuthenticated , IsCustomUser ]
    #     return super().get_permissions()
    
    

from geopy.geocoders import Nominatim
class ReportTransfer(APIView):
    queryset = [Sector.objects.all(), Report.objects.all()]
    serializer_classes = [ SectorSerializer, ReportSerializer,]
    permission_classes = (permissions.AllowAny,)
    # queryset = Report.objects.all().order_by("-postedAt")
    def get_queryset(self):
        report = Report.objects.all().order_by("-postedAt")
        sector = Sector.objects.all()
        return [report,sector]
    def put(self, request, *args, **kwargs):
        sec_type = request.data['sector_type']
        id =  request.data['report_id']
        
        print("IDDD: ",id)
        report = Report.objects.get(id=id)
        # sector = Sector.objects.filter("sector_type")
        if report:

            sector_location = report.location
            print(sector_location)
            qs = Sector.objects.filter(sector_type = sec_type)


            # pnt = sector_location
            # qs = qs.annotate(distance= Distance('location' , pnt)).filter(distance__lte=3000, sector_type=sec_type).order_by("-distance")
            if(qs):
                nearby_sector = qs.first()
                if(nearby_sector):
                    report.sector = nearby_sector
                    report.save()
                    serializer = ReportSerializer(report)
                    
            # sector = Sector.objects.get(sector_type = sec_type)
            
                    return Response({"message": 'you transfered the report',"report":serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": 'No Sector Found'})
            else:
                return Response({"message": 'NO Nearby Sector Found'})
        else:
            return Response({"message": 'NO report Found'})
        
class ReportStatusView(APIView):
    # permission_classes = (IsAuthenticated, IsCustomUser)
    queryset = [Sector.objects.all(), User.objects.all(), Report.objects.all()]
    serializer_classes = [ SectorAdminSerializer, SectorSerializer, ReportSerializer, LocationSerializer]
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request, pk=None):
        # id = self.kwargs.get("pk")
        
        role = Role.objects.get(id=2)
        sector_user = User.objects.get(id=pk,roles=role)
        if sector_user:
            # ser = SectorAdminSerializer(sector_user)
            sector_branch = sector_user.sector
            sector_type = sector_user.sector.sector_type
            if sector_type:
                sectors = Sector.objects.filter(sector_type=sector_type)
                
                branches = sectors.count()
                ser = SectorSerializer(sectors, many=True)
                active_report_count = Report.objects.filter(state=False,sector=sector_branch).count()
                resolved_report_count = Report.objects.filter(state=True, sector=sector_branch).count()
                spam_report_count = Report.objects.filter(spamStatus=True,sector=sector_branch).count()

                sectro = Sector.objects.get(id=7)
                sec_loc = LocationSerializer(sectro)
                lela2 = sectro.location.coords[1]
                lela = round(lela2, 6)
                # geolocator = Nominatim(user_agent="geoapiExercises")
              
                # Latitude = "12.211180"
                # Longitude = "34.804687"
  
                # location = geolocator.reverse(Latitude+","+Longitude)
                # if location:
                #     address = location.raw['address']
                #     city = address.get('city', '')
                #     state = address.get('state', '')
                #     country = address.get('country', '')
                #     return JsonResponse({"loc":sec_loc.data,"country":country, "city":city, "lela":lela})
                # ser = SectorSerializer(branches, many=True)
                return JsonResponse({"sectors":ser.data,"count":{"branch_count":[branches,"Branch Number"], "active_report":[active_report_count,"Active Reports"],"resolved_report":[resolved_report_count,"Resolved Reports"], "spam_report":[spam_report_count,"Spam Reports"]}})
            else:
                return JsonResponse({"error":"NO Sectors with this account"})
        else:
            return JsonResponse({"error":"No Data"})

        
class LikeReportView(APIView):
    # permission_classes = (IsAuthenticated, IsCustomUser)
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        id = self.kwargs.get("pk")
        report = Report.objects.get(id=id)
        if report.noOfLikes.filter(id=request.user.id).exists():
            report.noOfLikes.remove(request.user)
            return Response({"message": 'you disliked the report'}, status=status.HTTP_201_CREATED)
            
        else:
            report.noOfLikes.add(request.user.id)
            return Response({"message": 'you liked the report'}, status=status.HTTP_201_CREATED)
        

class ChartDataView(APIView):
    # permission_classes = (IsAuthenticated , IsSectorAdmin)
    permission_classes = (permissions.AllowAny,)

    def get_amount_for_source(self, reports, source):
        reports = reports.filter(title = source)
        amount = reports.count()
        # for i in reports:
        #     amount+=i.amount
        return {'amount':str(amount)}
    def get_source(self, report):
        return report.title

    # def get2(self , request , format=None):
    #     todayy = datetime.date.today()
    #     ayear_ago = todayy - datetime.timedelta(days = 30*12)
    #     recived_count = Report.objects.filter(postedAt__gte=ayear_ago, postedAt__lte=todayy).count()

    #     final = {}
    #     # sources = list(set(map(self.get_source, recived_count)))

    #     # for i in recived_count:
    #     #     for source in sources:
    #     #         final[source] = self.get_amount_for_source(recived_count, source)
    #     return Response({"Statistic: ":recived_count})
    def get(self , request , format=None):



        startdate = self.request.query_params.get('startdate', "2022-04-01T21:12:33.047056Z")
        # startdate = "2022-04-01T23:12:33.047056Z"
        enddate = self.request.query_params.get('enddate', None)
        # startdate = self.request.query_params.get('enddate', "2022-04-01T23:12:33.047056Z")
        # enddate = datetime.today()
        districtname = self.request.query_params.get('dname','Addis Ababa Water And Sewage Authority')
        # districtname = 'Addis Ababa Water And Sewage Authority'
        recived_count = Report.objects.filter(sector__district_name=districtname,postedAt__range=[enddate, startdate]).count()
        resolved_count  = Report.objects.filter(sector__district_name=districtname,state=True , postedAt__range=[enddate, startdate]).count()
        unresolved_count = Report.objects.filter(sector__district_name=districtname, state=False , postedAt__range=[enddate, startdate]).count()
        labeles = ["Recievd" , "Resolved" , "UnResolved"]
        default_items = [recived_count , resolved_count , unresolved_count]
        data = {
            "labels" : labeles,
            "default": default_items
        }
        return Response(data)
    
    
    
    
class MyReportAPIView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    permission_classes = (IsAuthenticated,IsCustomUser )
    http_method_names = ['get', 'patch']
    serializer_class = ReportSerializer
    pagination_class = PageNumberPagination
    queryset = Report.objects.all().order_by("-postedAt")
    
    
     
    def list(self, request, *args, **kwargs):
        report = Report.objects.filter(user=self.request.user).order_by("-postedAt")
        serializer = ReportSerializer(report , many= True)
        return Response(serializer.data)
    
    def partial_update(self, request, pk=None):
        id = self.kwargs.get("pk")
        try:
            report = Report.objects.filter(user=self.request.user).get(id=id)
            reportserializer = MyReportUpdateSerializer(report, data=request.data, partial=True)
            if reportserializer.is_valid():
                reportserializer.save()
                return Response(reportserializer.data, status=status.HTTP_200_OK)
            return Response(reportserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Report.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
  

    
    
    
    
    

        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
   

    
    