from rest_framework.views import APIView
from .models import Report
from .serializers import ReportSerializer ,ReportUpdateSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from permissions import IsSectorAdmin , IsCustomUser, IsSuperAdmin
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance



class ReportAPIView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,IsSectorAdmin )
    http_method_names = ['get', 'post', 'patch']
    serializer_class = ReportSerializer
    pagination_class = PageNumberPagination
    queryset = Report.objects.all().order_by("-postedAt")
    def get_queryset(self):
        report = Report.objects.all().order_by("-postedAt")
        return report
    
    def create(self, request, **kwargs):
        latitude = request.data['latitude']
        longtiude = request.data['longtiude']
        pnt = GEOSGeometry('POINT(%s %s)' % (longtiude, latitude))
        serializer_obj = ReportSerializer(data=request.data)
        
        if serializer_obj.is_valid():
            serializer_obj.save(location=pnt)
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
        if self.action in [ 'partial_update', 'destroy', ]:
            self.permission_classes = [IsAuthenticated, IsSectorAdmin]
        elif self.action in ['list' ,]:
            self.permission_classes = [IsAuthenticated  ]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated , IsCustomUser ]
        return super().get_permissions()
    
    



class LikeReportView(APIView):
    permission_classes = (IsAuthenticated, IsCustomUser)
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
    permission_classes = (IsAuthenticated , IsSectorAdmin)
    def get(self , request , format=None):
        startdate = self.request.query_params.get('startdate', None)
        enddate = self.request.query_params.get('enddate', None)
        districtname = self.request.query_params.get('dname')
        recived_count = Report.objects.filter(sector__district_name=districtname,postedAt__range=[startdate, enddate]).count()
        resolved_count  = Report.objects.filter(sector__district_name=districtname,state=True , postedAt__range=[startdate, enddate]).count()
        unresolved_count = Report.objects.filter(sector__district_name=districtname, state=False , postedAt__range=[startdate, enddate]).count()
        labeles = ["Recievd" , "Resolved" , "UnResolved"]
        default_items = [recived_count , resolved_count , unresolved_count]
        data = {
            "labels" : labeles,
            "default": default_items
        }
        return Response(data)
    
    

        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
   

    
    