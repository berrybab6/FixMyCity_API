# from django.urls import path
# from django.urls import include
# from .views import ReportAPIView


# app_name = "report"

# urlpatterns = [
#     path('report/', ReportAPIView.as_view()),
#     path('report/<int:pk>/', ReportAPIView.as_view()),
#     path('api/', include('rest_framework.urls')),
    

   
# ]



from rest_framework import routers
from .views import ReportAPIView ,LikeReportView , ChartDataView, ReportStatusView
from django.urls import path, include

app_name = 'report'


router = routers.DefaultRouter()


router.register('report', viewset=ReportAPIView, basename='report')
# router.register('chart', viewset=ChartDataView, basename='chart')

urlpatterns = [
    path('', include(router.urls )),
    path('like/<int:pk>' ,LikeReportView.as_view()),
    path('chart' ,ChartDataView.as_view()),
    path("report_status/<int:pk>/",ReportStatusView.as_view())
]