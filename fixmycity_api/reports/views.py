from dis import dis
from tracemalloc import start
from turtle import distance
from rest_framework.views import APIView
from .models import F, Report
from .serializers import ReportSerializer ,ReportUpdateSerializer, MyReportUpdateSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from permissions import IsSectorAdmin , IsCustomUser, IsSuperAdmin
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from .apps import ReportsConfig
from rest_framework.decorators import action



class ReportAPIView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = []
    # permission_classes = (IsAuthenticated,IsSectorAdmin )
    http_method_names = ['get', 'post', 'patch']
    serializer_class = ReportSerializer
    pagination_class = PageNumberPagination
    queryset = Report.objects.all().order_by("-postedAt")
    def get_queryset(self):
        report = Report.objects.all().order_by("-postedAt")
        return report
    
    @action(detail=False)
    def getreportbasedonSectorName(self , request):
        sector_name=self.request.user.sector
        print(sector_name)
        report = Report.objects.filter(sector__district_name=sector_name).order_by("-postedAt")
        serializer = ReportSerializer(report , many= True)
        return Response(serializer.data)
    
    
    @action(detail=False)
    def getreportbasedonSectorNameandLocation(self , request):
        sector_name=self.request.user.sector
        sector_location = self.request.user.sector.location
        print(sector_location)
        qs = super().get_queryset()
        pnt = sector_location
        qs = qs.annotate(distance= Distance('location' , pnt)).filter(distance__lte=3000 ,sector__district_name=sector_name ).order_by("-postedAt")
        serializer = ReportSerializer(qs , many= True)
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
        serializer = ReportSerializer(report , many= True)
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
            report = Report.objects.get(id=id)
            reportserializer = ReportUpdateSerializer(report, data=request.data, partial=True)
            if reportserializer.is_valid():
                reportserializer.save()
                return Response(reportserializer.data, status=status.HTTP_200_OK)
            return Response(reportserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Report.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
        
        
    
    def destroy(self, request, pk=None):
        id = self.kwargs.get("pk")
        try:
            report = Report.objects.get(pk=id)
            report.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Report.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
        
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in [ 'partial_update', 'destroy', 'getreportbasedonSectorName' , 'getreportbasedonSectorNameandLocation']:
            self.permission_classes = [IsAuthenticated, IsSectorAdmin]
        elif self.action in ['list' ,]:
            self.permission_classes = [IsAuthenticated  ]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated , IsCustomUser ]
        return super().get_permissions()
    
    



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
    
  

    
    
    
    
    

        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
   

    
    