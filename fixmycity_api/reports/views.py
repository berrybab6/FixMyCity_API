from dis import dis
from math import fabs
import re
from tracemalloc import start
from turtle import distance
import requests
from rest_framework.views import APIView
from .models import F, Report
from .serializers import LocationSerializer, ReportLikeSerializer, ReportSerializer ,ReportUpdateSerializer, MyReportUpdateSerializer
from django.http import JsonResponse
from accounts.models import Role, Sector, User
from accounts.serializers import SectorAdminSerializer, SectorSerializer


# from .serializers import LocationSerializer, ReportSerializer ,ReportUpdateSerializer
import httplib2
from requests import ConnectionError
import requests
import json
import time
import os
from fcm_django.models import FCMDevice
connection_timeout = 30 # seconds

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
from pyfcm import FCMNotification
from firebase_admin.messaging import Message, Notification


import requests

import datetime

class ReportAPIView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    # authentication_classes = []
    # permission_classes = (IsAuthenticated,IsSectorAdmin )
    
    http_method_names = ['get', 'post', 'patch' , 'delete' ]
    serializer_class = ReportSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ('id' , 'state' , 'status' , 'spamStatus',)
    search_fields = ('tag' , 'description' , 'user__first_name', 'user__last_name', 'sector__district_name' , 'user__phone_number')
    # ordering = ('noOfLikes',)
    queryset = [Report.objects.all().order_by("-updatedAt"), User.objects.all()]
    def get_queryset(self):
        report = Report.objects.all().order_by("-updatedAt")
        return report
    
    @action(detail=False)
    def getreportbasedonSectorName(self , request):
        sector_name=self.request.user.sector
        print(sector_name)
        report = Report.objects.filter(sector__district_name=sector_name).order_by("-updatedAt")
        serializer = ReportSerializer(report , many= True)
        # serializer = ReportSerializer(self.filter_queryset(self.get_queryset()), many=True,)
        return Response(serializer.data)
    
    
    @action(detail=False)
    def getreportbasedonSectorNameandLocation(self , request):
        sector_name=self.request.user.sector
        sector_location = self.request.user.sector.location
        print(sector_location)
        qs = super().get_queryset()
        pnt = sector_location
        qs = qs.annotate(distance= Distance('location' , pnt)).filter(distance__lte=3000 ,sector__district_name=sector_name ).order_by("-updatedAt")
        serializer = ReportSerializer(self.filter_queryset(self.get_queryset()), many=True,)
        # serializer = ReportSerializer(qs , many= True)
        return Response(serializer.data)
    
    @action(detail=False)
    def getReportChartView(self, request):
        zare = datetime.date.today()
        year = 2022
        month = 0

        a_year_ago = zare - datetime.timedelta(days=30*12)
        
        reports_by_month = {}
        for i in range(1,13):
            try:
                if Report.objects.filter(postedAt__year__gte=year,
                              postedAt__month=i).exists():
                    reports = Report.objects.filter(
                            postedAt__year=year,
                              postedAt__month=i)
                    reports_m = {}

                    if reports.filter(status="UNRESOLVED").exists():

                        unresolved = reports.filter(status="UNRESOLVED").count()
                        reports_m["unresolved"] = unresolved
                    if reports.filter(spamStatus=True).exists():
                        spamStatus=  reports.filter(spamStatus=True).count()
                        reports_m["spam_status"] = spamStatus
                    if reports.filter(status="RESOLVED").exists():
                        resolved = reports.filter(status="RESOLVED").count()
                        reports_m["resolved"] = resolved
                    name = "month_"+str(i)
                    reports_by_month[name] = reports_m
            except Exception as e:
                return False
        return JsonResponse({"response":reports_by_month})

    def send_spam_image(self,image):
        if image:
            
            url = 'https://fixmycity-ai.herokuapp.com/api/imageClassify/'
            start_time = time.time()
            while True:
                try:
                    get_updates = json.loads(requests.get(url).content)
                    response = requests.get(url)
                    data = {
                        "image": image
                     }

      
                    print("this is json data",data)
                
                    api_call = requests.post(url= url,data=data)
                    
                    
                    print(api_call.json())
                    is_spam = api_call.json().get("spam")
                    print("Is Spam:",is_spam)
                    return is_spam
                except ConnectionError:
                    if time.time() > start_time + connection_timeout:
                        raise Exception('Unable to get updates after {} seconds of ConnectionErrors'.format(connection_timeout))
                    else:
                        time.sleep(1) 
       
        else:
            print('Web site exists')

            return JsonResponse({"Me":"Hello"})
        
           
            
    
    
    
    def create(self, request, **kwargs):
        latitude = request.data['latitude']
        longtiude = request.data['longtiude']
        pnt = GEOSGeometry('POINT(%s %s)' % (longtiude, latitude))
       
        image = request.data['image']
        # lin_reg_model = ReportsConfig.model
        # image_predicted = lin_reg_model.predict(image)
        if image:
            user_c=self.request.user.id
            # print("User", self.request.user.phone_number)
            if  User.objects.filter(id = user_c).exists():
                user = User.objects.get(id = self.request.user.id)
                if not user.is_banned:
                    serializer_obj = ReportSerializer(data=request.data)

                    if serializer_obj.is_valid():
                        serializer_obj.save(location=pnt , spamStatus=True)

                        img = serializer_obj.data["image"]
                        print("IMG",img)
                        spam = self.send_spam_image(img)
                        # print("sPAMMMMm:",spam)
                        image_predicted = 1
                        image_predicted = spam
                        if image_predicted == 1:
                            # serializer_obj = ReportSerializer(data=request.data)
                            if serializer_obj.is_valid():
                                # serializer_obj.save(location=pnt , spamStatus=True)
                                # serializer_obj.data["spamStatus"] = True
                                print("IS___Spam",serializer_obj.data["id"])
                                id = serializer_obj.data["id"]
                                report = Report.objects.get(id=id)
                                
                                report.spamStatus= True
                                report.save()
                                user = User.objects.get(id=report.user.id)
                                if user: 
                                    user.count_strike = user.count_strike+1
                                    if user.count_strike >= 3:
                                        user.is_banned = True
                                    else:
                                        pass
                                    user.save() 
                                print("Statusss-",report.spamStatus)
                                return Response({"detail": 'Data Created'}, status=status.HTTP_200_OK)
                            return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
                        elif image_predicted==0:
                            # serializer_obj = ReportSerializer(data=request.data , )
                            if serializer_obj.is_valid():
                                # serializer_obj.save(location=pnt , spamStatus=False)
                                id = serializer_obj.data["id"]
                                report = Report.objects.get(id=id)
                                
                                report.spamStatus= False
                                report.save()
                                return Response({"detail": 'NonSpam Data Created'}, status=status.HTTP_201_CREATED)
                            else:
                                return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": 'Unable to make Connection'}, status=status.HTTP_201_CREATED)

                    else:
                        return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)  
                else:
                    return JsonResponse({"message":"User Has Been Banned"},status=status.HTTP_403_FORBIDDEN)
                
            else:
                return  JsonResponse({"error":"User Doesnot Exist"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return  JsonResponse({"error":"Image is not UPloaded"},status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    
    
    # def create(self, request, **kwargs):
    #     latitude = request.data['latitude']
    #     longtiude = request.data['longtiude']
    #     pnt = GEOSGeometry('POINT(%s %s)' % (longtiude, latitude))
       
    #     image = request.data['image']
    #     # lin_reg_model = ReportsConfig.model
    #     # image_predicted = lin_reg_model.predict(image)
    #     if image:
    #         serializer_obj = ReportSerializer(data=request.data)

    #         if serializer_obj.is_valid():
    #             serializer_obj.save(location=pnt , spamStatus=True)

    #             img = serializer_obj.data["image"]
    #             print("IMG",img)
    #             spam = self.send_spam_image(img)
    #             print("sPAMMMMm:",spam)
    #             image_predicted = spam
    #             if image_predicted == 1:
    #                 # serializer_obj = ReportSerializer(data=request.data)
    #                 if serializer_obj.is_valid():
    #                     # serializer_obj.save(location=pnt , spamStatus=True)
    #                     # serializer_obj.data["spamStatus"] = True
    #                     print("IS___Spam",serializer_obj.data["id"])
    #                     id = serializer_obj.data["id"]
    #                     report = Report.objects.get(id=id)
                        
    #                     report.spamStatus= True
    #                     report.save()
    #                     user = User.objects.get(id=report.user.id)
    #                     if user: 
    #                         user.count_strike = user.count_strike+1
    #                         if user.count_strike >= 3:
    #                             user.active = False
    #                         else:
    #                             pass
    #                         user.save() 
    #                     print("Statusss-",report.spamStatus)
    #                     return Response({"detail": 'you created spam report' }, status=status.HTTP_200_OK)
    #                 return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
    #             elif image_predicted==0:
    #                 id = serializer_obj.data["id"]
    #                 report = Report.objects.get(id=id)
                        
    #                 report.spamStatus= False
    #                 report.save()
                    
    #                 # serializer_obj = ReportSerializer(data=request.data , )
    #                 # if serializer_obj.is_valid():
    #                     # serializer_obj.save(location=pnt , spamStatus=False)
                        
    #                 return Response({"detail": 'Data Created'}, status=status.HTTP_201_CREATED)
    #                 # return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    # def create(self, request, **kwargs):
        
    #     latitude = request.data['latitude']
    #     longtiude = request.data['longtiude']
    #     pnt = GEOSGeometry('POINT(%s %s)' % (longtiude, latitude))
    #     serializer_obj = ReportSerializer(data=request.data)
    #     image = request.data['image']
    #     # lin_reg_model = ReportsConfig.model
    #     # image_predicted = lin_reg_model.predict(image)
    #     self.send_spam_image(image)
    #     image_predicted = 0
    #     if image_predicted == 1:
    #         serializer_obj = ReportSerializer(data=request.data)
    #         if serializer_obj.is_valid():
    #             serializer_obj.save(location
    #                                 =pnt , spamStatus=True)
    #             return Response({"detail": 'Data Created'}, status=status.HTTP_201_CREATED)
    #         return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         serializer_obj = ReportSerializer(data=request.data , )
    #         if serializer_obj.is_valid():
    #             serializer_obj.save(location=pnt , spamStatus=False)
    #             return Response({"detail": 'Data Created'}, status=status.HTTP_201_CREATED)
    #         return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
            
    
    
    
    

    
    def list(self, request, *args, **kwargs):
        report = Report.objects.all().order_by("-updatedAt")
        # serializer = ReportSerializer(report , many= True)
        serializer = ReportSerializer(self.filter_queryset(self.get_queryset()), many=True,)
        
        qs = super().get_queryset()
      
        latitude = self.request.query_params.get('lat', None)
        longtiude = self.request.query_params.get('lng', None)
        if latitude and longtiude:
            pnt = GEOSGeometry('POINT(%s %s)' % (longtiude, latitude) , srid=4326)
            distance = Distance('location' , pnt)
            qs = qs.annotate(distance= Distance('location' , pnt)).filter(distance__lte=3000).order_by("-updatedAt")
            serializer = ReportSerializer(qs , many= True)
        return Response(serializer.data)
        

    
    
    
    
    
    def partial_update(self, request, pk=None):
        id = self.kwargs.get("pk")
        try:
            
            # print(self.request.user.sector)
            #  announcment = Announcement.objects.filter(sectoradmin__sector_user=self.request.user).get(id=id)
            # report = Report.objects.filter(sector__district_name=self.request.user.sector).get(id=id)
            report = Report.objects.get(id=id)
            is_spam = report.spamStatus
            spamStat = request.data.get("spamStatus",False)

            if spamStat:
                if User.objects.filter(id=report.user.id).exists():
                    user = User.objects.get(id=report.user.id)
                    user.count_strike = user.count_strike + 1
                    if user.count_strike >=3:
                        user.is_banned = True
                    user.save()
            elif (not (spamStat == is_spam)):
                if User.objects.filter(id=report.user.id).exists():
                    user = User.objects.get(id=report.user.id)
                    user.count_strike = user.count_strike - 1
                    user.save()
            else: 
                pass    
            

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
        
        
        
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in [ 'partial_update', 'destroy', 'getreportbasedonSectorName' , 'getreportbasedonSectorNameandLocation']:
            self.permission_classes = [IsAuthenticated, IsSectorAdmin]
        elif self.action in ['list' , 'retrieve']:
            self.permission_classes = [IsAuthenticated  ]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated , IsCustomUser ]
        return super().get_permissions()
    
    
    

from geopy.geocoders import Nominatim
class ReportTransfer(APIView):
    queryset = [Sector.objects.all(), Report.objects.all()]
    serializer_classes = [ SectorSerializer, ReportSerializer,]
    permission_classes = (IsAuthenticated, IsSectorAdmin)
    # queryset = Report.objects.all().order_by("-postedAt")
    def get_queryset(self):
        report = Report.objects.all().order_by("-updatedAt")
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
    # def get_permissions(self):
    #     """Set custom permissions for each action."""
    #     if self.action in [ 'partial_update', 'destroy', 'getreportbasedonSectorName' , 'getreportbasedonSectorNameandLocation']:
    #         self.permission_classes = [IsAuthenticated, IsSectorAdmin]
    #     elif self.action in ['list' , 'retrieve']:
    #         self.permission_classes = [IsAuthenticated  ]
    #     elif self.action in ['create']:
    #         self.permission_classes = [IsAuthenticated , IsCustomUser ]
    #     return super().get_permissions()
    
    
        
class ReportStatusView(APIView):
    # permission_classes = (IsAuthenticated, IsCustomUser)
    queryset = [Sector.objects.all(), User.objects.all(), Report.objects.all()]
    serializer_classes = [ SectorAdminSerializer, SectorSerializer, ReportSerializer, LocationSerializer]
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        # id = self.kwargs.get("pk")
        
        role = Role.objects.get(id=2)
        sector_user = self.request.user

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

                # sectro = Sector.objects.get(id=7)
                # sec_loc = LocationSerializer(sectro)
                # lela2 = sectro.location.coords[1]
                # lela = round(lela2, 6)

                return JsonResponse({"sectors":ser.data,"count":{"branch_count":[branches,"Branch Number"], "active_report":[active_report_count,"Active Reports"],"resolved_report":[resolved_report_count,"Resolved Reports"], "spam_report":[spam_report_count,"Spam Reports"]}})
            else:
                return JsonResponse({"error":"NO Sectors with this account"})
        else:
            return JsonResponse({"error":"No Data"})

        
class LikeReportView(APIView):
    
    def put(self, request, pk=None):
        id = self.kwargs.get("pk")
        try:
            report = Report.objects.get(id=id)
            reportserializer = ReportLikeSerializer(report, data=request.data, partial=True)
            if reportserializer.is_valid() and report.noOfLikes.filter(id=request.user.id).exists():
                
                reportserializer.save(likeornot="False")
                serializer = ReportLikeSerializer(report)
                report.noOfLikes.remove(request.user)
                

                return Response({"message": 'you disliked the report' , "data": serializer.data },  status=status.HTTP_201_CREATED)
            # return Response(reportserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            elif reportserializer.is_valid() and  not report.noOfLikes.filter(id=request.user.id).exists():
               
                reportserializer.save(likeornot="True")
                serializer = ReportLikeSerializer(report)
                report.noOfLikes.add(request.user)
               

                return Response({"message": 'you liked the report' , "data": serializer.data },  status=status.HTTP_201_CREATED)
            # return Response(reportserializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Report.DoesNotExist:
            return Response({"detail" : 'Report does not exist or you dont have permission to update it'} , status=status.HTTP_404_NOT_FOUND)
        
        
    
    
    
    # permission_classes = (IsAuthenticated, IsCustomUser)
    # permission_classes = (permissions.AllowAny,)
    # def post(self, request, *args, **kwargs):
    #     id = self.kwargs.get("pk")
    #     report = Report.objects.get(id=id)
    #     if report.noOfLikes.filter(id=request.user.id).exists():
    #         reportserializer = ReportLikeSerializer(report, data=request.data)
    #         if reportserializer.is_valid():
    #             reportserializer.save()
    #             serializer = ReportLikeSerializer(report)
    #             report.noOfLikes.remove(request.user)
                
           
    #         return Response({"message": 'you disliked the report' , "data": serializer.data },  status=status.HTTP_201_CREATED)
            
    #     else:
    #         reportserializer = ReportLikeSerializer(report, data=request.data)
            
    #         if reportserializer.is_valid():
    #             reportserializer.save()
    #             serializer = ReportLikeSerializer(report)
    #             report.noOfLikes.add(request.user.id)
                
    #         return Response({"message": 'you liked the report' ,  "data": serializer.data}, status=status.HTTP_201_CREATED)
        

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
    queryset = Report.objects.all().order_by("-updatedAt")
    
    
     
    def list(self, request, *args, **kwargs):
        report = Report.objects.filter(user=self.request.user).order_by("-updatedAt")
        serializer = ReportSerializer(report , many= True)
        return Response(serializer.data)
    
    def partial_update(self, request, pk=None):
        id = self.kwargs.get("pk")
        try:
            report = Report.objects.filter(user=self.request.user).get(id=id)
            reportserializer = MyReportUpdateSerializer(report, data=request.data, partial=True)
            if reportserializer.is_valid():
                reportserializer.save()
                return Response({"detail": "Data Updated!"}, status=status.HTTP_200_OK)
            return Response(reportserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Report.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    
    
    
    
    
class sendNotifications(APIView): 
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            title = "hello"
            desc = "hu"
            action = None
        try:
            action = request.POST['Action']
        except:
            print('action is empty')
        # upload image
        isEmpty = True
        # try:
        #     img = request.FILES['image']
        #     isEmpty = False

        #     try:
        #         imageObject = notification_image.objects.get(id=1)
        #         imageObject.image = img
        #         # save img
        #         imageObject.save()
        #         print('update')
        #     except notification_image.DoesNotExist:
        #         print('create')
        #         notification_image.objects.create(image=img)
        # except:
        #     print('')

            # get image
        print(isEmpty)

        # image = notification_image.objects.all()
        # all token
        # tokens = user_push_token.objects.all()
        # all token array
        alltokens = []
        # image
        push_img = {}
        # for tokenlist in tokens:
        #     alltokens.append(tokenlist.token)
        # if image:
        #     push_img = {'image': image[0].image.url}
        # FCMManager.sendPush(title, desc, alltokens, push_img)
        if isEmpty:
            data_message = {
                "title": title,
                "body": desc,
                "action": action,
                "image": None,
            }
        # else:
        #     data_message = {
        #         "title": title,
        #         "body": desc,
        #         "action": action,
        #         "image": '{}'.format(request._current_scheme_host + image[0].image.url),
        #     }

        # print(image[0].image.url)
        print(data_message)
        push_service = FCMNotification(
            api_key="AAAA8F809G4:APA91bHwmFnvJmaQySM7oZSivwiDm_MYHdJTLruZPLNL2zXfzR71NjBSe6mbpozAvsFEupwL8fsfZGt-GSPuMCdwuizHsNUwAgk4JW20BBu6ZQwjDj3DK5aKRxrdCu3InKy5_Ro4_yq1")

        try:
            check = request.POST['check']
            tokens = request.POST['token']
            registration_ids = [tokens]
            print(check, tokens)
            result = push_service.multiple_devices_data_message(registration_ids=registration_ids,
                                                                data_message=data_message)
            print(result)
            return Response({"detail": "Data Updated!"}, status=status.HTTP_200_OK)
        except:
            print('not check')

        registration_ids = alltokens
        result = push_service.multiple_devices_data_message(registration_ids=registration_ids,
                                                            data_message=data_message)
        print(result)

        return Response({"detail": "Data Updated!"}, status=status.HTTP_200_OK)
    # else:
    # #   allcountry =  push_token_countryList.objects.all()
    #   return Response({"detail": "Data Updated!"}, status=status.HTTP_200_OK)





def notif(request):
    FCMDevice.objects.send_message(Message(data=dict()))
# Note: You can also combine the data and notification kwarg
    FCMDevice.objects.send_message(
    Message(notification=Notification(title="title", body="body", image="image_url"))
     )
    device = FCMDevice.objects.filter(1==1)
    device.send_message(Message(...))
    return JsonResponse({'status':'OK'})
    # devices = FCMDevice.objects.filter(user__phone_number='+251962782800')
    # print("here", devices)
    # for device in devices:
    #    device.send_message(title="Title", body="Body", data={"test": "test"})
    #    print(devices)
    #    break

    # return JsonResponse({'status':'OK'})



  

         
    
    
         
      
    
    
    
    
    
    
    
# def sendNotifications(request):
#     if request.method == 'POST':
#         title = request.POST['Title']
#         desc = request.POST['Descriptions']
#         action = None
#         try:
#             action = request.POST['Action']
#         except:
#             print('action is empty')
#         # upload image
#         isEmpty = True
#         # try:
#         #     img = request.FILES['image']
#         #     isEmpty = False

#         #     try:
#         #         imageObject = notification_image.objects.get(id=1)
#         #         imageObject.image = img
#         #         # save img
#         #         imageObject.save()
#         #         print('update')
#         #     except notification_image.DoesNotExist:
#         #         print('create')
#         #         notification_image.objects.create(image=img)
#         # except:
#         #     print('')

#             # get image
#         print(isEmpty)

#         # image = notification_image.objects.all()
#         # all token
#         # tokens = user_push_token.objects.all()
#         # all token array
#         alltokens = []
#         # image
#         push_img = {}
#         # for tokenlist in tokens:
#         #     alltokens.append(tokenlist.token)
#         # if image:
#         #     push_img = {'image': image[0].image.url}
#         # FCMManager.sendPush(title, desc, alltokens, push_img)
#         if isEmpty:
#             data_message = {
#                 "title": title,
#                 "body": desc,
#                 "action": action,
#                 "image": None,
#             }
#         # else:
#         #     data_message = {
#         #         "title": title,
#         #         "body": desc,
#         #         "action": action,
#         #         "image": '{}'.format(request._current_scheme_host + image[0].image.url),
#         #     }

#         # print(image[0].image.url)
#         print(data_message)
#         push_service = FCMNotification(
#             api_key="AAAA8F809G4:APA91bHwmFnvJmaQySM7oZSivwiDm_MYHdJTLruZPLNL2zXfzR71NjBSe6mbpozAvsFEupwL8fsfZGt-GSPuMCdwuizHsNUwAgk4JW20BBu6ZQwjDj3DK5aKRxrdCu3InKy5_Ro4_yq1")

#         try:
#             check = request.POST['check']
#             tokens = request.POST['token']
#             registration_ids = [tokens]
#             print(check, tokens)
#             result = push_service.multiple_devices_data_message(registration_ids=registration_ids,
#                                                                 data_message=data_message)
#             print(result)
#             return Response({"detail": "Data Updated!"}, status=status.HTTP_200_OK)
#         except:
#             print('not check')

#         registration_ids = alltokens
#         result = push_service.multiple_devices_data_message(registration_ids=registration_ids,
#                                                             data_message=data_message)
#         print(result)

#         return Response({"detail": "Data Updated!"}, status=status.HTTP_200_OK)
#     else:
#     #   allcountry =  push_token_countryList.objects.all()
#       return Response({"detail": "Data Updated!"}, status=status.HTTP_200_OK)

  

    
    
    
    
    

        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
   

    
    