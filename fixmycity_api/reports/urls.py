from django.urls import path
from django.urls import include
from .views import ReportAPIView


app_name = "report"

urlpatterns = [
    path('report/', ReportAPIView.as_view()),
    path('report/<int:pk>/', ReportAPIView.as_view()),
    path('api/', include('rest_framework.urls')),
    

   
]
