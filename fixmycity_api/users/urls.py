from django.urls import path
from django.urls import include
from .views import ValidatePhoneSendOTP , ValidateOTP ,  Register , LoginAPI , ValidateLoginOTP , LoginView


app_name = "users"

urlpatterns = [
    path('validate_phone/', ValidatePhoneSendOTP.as_view()),
    path('validate_otp/', ValidateOTP.as_view()),
    path('registor/', Register.as_view()),
    path('validate_login_otp/', ValidateLoginOTP.as_view()),
    path('login/', LoginView.as_view()),
    path('api/', include('rest_framework.urls')),

   
]
