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
from .views import ReportAPIView
from django.urls import path, include

app_name = 'report'


router = routers.DefaultRouter()

router.register('report', viewset=ReportAPIView, basename='report')

urlpatterns = [
    path('', include(router.urls ))
]