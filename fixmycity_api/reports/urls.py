from rest_framework import routers

from .views import ReportAPIView ,LikeReportView , ChartDataView , MyReportAPIView, ReportStatusView, notif, sendNotifications

from django.urls import path, include
from . import views
app_name = 'report'


router = routers.DefaultRouter()


router.register('report', viewset=ReportAPIView, basename='report')
router.register('myreport', viewset=MyReportAPIView, basename='myreport')

urlpatterns = [
    path('', include(router.urls )),
    path('like/<int:pk>' ,LikeReportView.as_view()),

    path('chart' ,ChartDataView.as_view()),
    path('transfer/', views.ReportTransfer.as_view()),
    path("report_status/",ReportStatusView.as_view()),
    path('send_notifications/', notif),
    
    

]