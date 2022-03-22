import re
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Report
from .serializers import ReportSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from  permissions import IsSectorAdmin , IsCustomUser



class ReportAPIView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,IsSectorAdmin )
    serializer_class = ReportSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        report = Report.objects.all().order_by("-postedAt")
        print(report)
        return report
    
    def create(self, request):
        serializer_obj = ReportSerializer(data=request.data)
        
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response({"msg": 'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    
    
    
    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        print(params["pk"])
        report = Report.objects.all()
        serializer = ReportSerializer(report , many= True)
        return Response(serializer.data)
    
    
    
    
    
    
    
        
        
    def partial_update(self, request, pk=None):
        id = self.kwargs.get("pk")
        try:
            report = Report.objects.get(id=id)
            reportserializer = ReportSerializer(report, data=request.data, partial=True)
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
        elif self.action in ['list' , 'retrieve']:
            self.permission_classes = [IsAuthenticated  ]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated , IsCustomUser ]
        return super().get_permissions()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   

    
    