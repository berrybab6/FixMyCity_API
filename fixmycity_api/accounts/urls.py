# from django.contrib import admin
from django import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# # from django.views.decorators.csrf import csrf_exempt
# # from graphene_file_upload.django import FileUploadGraphQLView

from django.urls import include

from .views import ActiveSectorCount, BanCustomUserAPIView, CustomUserAPIView, EditProfile, LoginView, MainSectorAPIView, RegisterView, LoginSerializer,SectorAPIView, SectorCount, TestView,  LoginSectorAdminView, UserCount, UserDetailView, UserView
from .views import EditProfile, LoginView, RegisterView, LoginSerializer, TestView, RoleView


from rest_framework import routers
app_name = 'accounts'
router = routers.DefaultRouter()

router.register('sector',SectorAPIView,basename='sector')
# router.register('users',CustomUserAPIView,basename='users')

# MainSectorAPIView

# router.register('main_sectors',MainSectorAPIView,basename='main sector')

# router.register('',SectorView,basename='Sector')
# router.register('role',SectorView,basename='Role')

# router.register('login',LoginView,basename='User')

urlpatterns = [
    path('register/', RegisterView.as_view()),

    path('sector/',include(router.urls)),
    path("roles/", RoleView.as_view(), name="User by role"),
    

    path('main_sectors/',MainSectorAPIView.as_view()),

    path('login/', LoginView.as_view()),
    path('login_sectoradmin/', LoginSectorAdminView.as_view()),
    
    path('api/', include('rest_framework.urls')),
    path('user_count/', UserCount.as_view()),
    path('sector_count/', SectorCount.as_view()),
    path('active_sectors/', ActiveSectorCount.as_view()),

    path('custom_users/',CustomUserAPIView.as_view()),
    path('custom_users/<int:pk>',BanCustomUserAPIView.as_view()),
    path('users/',UserView.as_view()),
    path('users/<int:pk>',UserDetailView.as_view()),
    # path('sector/',SectorView.as_view())
#     path('test/', TestView.as_view()),
#     path('edit/<int:id>/',EditProfile.as_view()),
]

# urlpatterns+= router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

