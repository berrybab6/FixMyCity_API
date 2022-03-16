# from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# from django.views.decorators.csrf import csrf_exempt
# from graphene_file_upload.django import FileUploadGraphQLView

from django.urls import include
from .views import EditProfile, LoginView, RegisterView, LoginSerializer, TestView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('api/', include('rest_framework.urls')),

    path('test/', TestView.as_view()),
    path('edit/<int:id>/',EditProfile.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

