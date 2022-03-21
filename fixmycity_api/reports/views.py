from django.shortcuts import render
from rest_framework.views import APIView
from .models import Report
from .serializers import ReportSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ReportAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get("pk")
        report = Report.objects.all()
        serializer = ReportSerializer(report, many=True)
        if id is not None:
            try:
                report = Report.objects.get(id=id)
                serializer = ReportSerializer(report)
                return Response(serializer.data)
            except Report.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)
    
    
    def post(self, request, *args, **kwargs):
        serializer_obj = ReportSerializer(data=request.data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response({"msg": 'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    def put(self, request, *args, **kwargs):
        id = self.kwargs.get("pk")
        try:
            report = Report.objects.get(id=id)
            reportserializer = ReportSerializer(report, data=request.data)
            if reportserializer.is_valid():
                reportserializer.save()
                return Response(reportserializer.data, status=status.HTTP_200_OK)
            return Response(reportserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Report.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    
    


    
    