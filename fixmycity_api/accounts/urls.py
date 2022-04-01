# from django.contrib import admin
from django import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# # from django.views.decorators.csrf import csrf_exempt
# # from graphene_file_upload.django import FileUploadGraphQLView

from django.urls import include
from .views import EditProfile, LoginView, RegisterView, LoginSerializer, TestView,SectorAPIView , LoginSectorAdminView
#
from rest_framework import routers
app_name = 'accounts'
router = routers.DefaultRouter()
router.register('sector',SectorAPIView,basename='sector')
# router.register('login',LoginView,basename='User')

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('',include(router.urls)),

    path('login/', LoginView.as_view()),
    path('login_sectoradmin/', LoginSectorAdminView.as_view()),
    
    path('api/', include('rest_framework.urls')),
    # path('sector/',SectorView.as_view())
#     path('test/', TestView.as_view()),
#     path('edit/<int:id>/',EditProfile.as_view()),
]

# urlpatterns+= router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

