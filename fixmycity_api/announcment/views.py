
from email import message
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Announcement
from .serializers import AnnouncementSerializer
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , BasePermission , SAFE_METHODS
from rest_framework import serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from permissions import IsSectorAdmin






class AnnouncementAPIView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,IsSectorAdmin )
    permission_classes = (permissions.AllowAny,)
    serializer_class = AnnouncementSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        announcment = Announcement.objects.all().order_by("-date")
        print(announcment)
        return announcment
    
    def create(self, request):
        serializer_obj = AnnouncementSerializer(data=request.data)
        
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response({"detail": 'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    
    
    
    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        print(params["pk"])
        announcment = Announcement.objects.filter(sector__district_name = params["pk"])
        serializer = AnnouncementSerializer(announcment , many= True)
        return Response(serializer.data)
    
    
    
    
    
    
    def update(self, request, pk=None):
        id = self.kwargs.get("pk")
        try:
           
            announcment = Announcement.objects.filter(sectoradmin__sector_user=self.request.user).get(id=id)
            announcmentserializer = AnnouncementSerializer(announcment, data=request.data)
            if announcmentserializer.is_valid() :
                
                announcmentserializer.save()
                return Response(announcmentserializer.data, status=status.HTTP_200_OK)
            return Response(announcmentserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Announcement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
        
        
        
        
    def partial_update(self, request, pk=None):
        id = self.kwargs.get("pk")
        try:
            announcment = Announcement.objects.filter(sectoradmin__sector_user=self.request.user).get(id=id)
            anouncmentserializer = AnnouncementSerializer(announcment, data=request.data, partial=True)
            if anouncmentserializer.is_valid():
                anouncmentserializer.save()
                return Response(anouncmentserializer.data, status=status.HTTP_200_OK)
            return Response(anouncmentserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Announcement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
        
        
    
    def destroy(self, request, pk=None):
        id = self.kwargs.get("pk")
        try:
            announcment = Announcement.objects.filter(sectoradmin__sector_user=self.request.user).get(pk=id)
            announcment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Announcement.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
        
    # def get_permissions(self):
    #     """Set custom permissions for each action."""
    #     if self.action in ['update', 'partial_update', 'destroy', 'create']:
    #         self.permission_classes = [IsAuthenticated, IsSectorAdmin]
    #     elif self.action in ['list' , 'retrieve']:
    #         self.permission_classes = [IsAuthenticated  ]
    #     return super().get_permissions()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   

