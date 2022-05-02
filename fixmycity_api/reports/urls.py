from rest_framework import routers

from .views import ReportAPIView ,LikeReportView , ChartDataView , MyReportAPIView, ReportStatusView

from django.urls import path, include

app_name = 'report'


router = routers.DefaultRouter()


router.register('report', viewset=ReportAPIView, basename='report')
router.register('myreport', viewset=MyReportAPIView, basename='myreport')

urlpatterns = [
    path('', include(router.urls )),
    path('like/<int:pk>' ,LikeReportView.as_view()),

    path('chart' ,ChartDataView.as_view()),
    path("report_status/<int:pk>/",ReportStatusView.as_view())

]