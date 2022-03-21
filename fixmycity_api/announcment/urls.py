# from django.urls import path
# from django.urls import include
# from .views import AnnouncementAPIView , AnnouncementBYSectorNameAPIView , TaskViewSet


# app_name = "announcement"

# urlpatterns = [
#     path('announcement/', AnnouncementAPIView.as_view()),
#     path('announcement/<int:pk>/', AnnouncementAPIView.as_view()),
#     path('announcementbyname/', TaskViewSet.as_view()),
    
  
#     path('api/', include('rest_framework.urls')),
    

   
# ]



from rest_framework import routers
from .views import AnnouncementAPIView
from django.urls import path, include

app_name = 'announcment'


router = routers.DefaultRouter()

router.register('announcment', viewset=AnnouncementAPIView, basename='announcment')

urlpatterns = [
    path('', include(router.urls ))
]