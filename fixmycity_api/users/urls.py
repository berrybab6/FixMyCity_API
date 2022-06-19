
from django.urls import path
from django.urls import include
from .views import Profileview, ValidatePhoneSendOTP ,RemoveFromBanUser ,  Register , Login , ValidateOTP , EditProfile


app_name = "users"

urlpatterns = [
    path('validate_phone/', ValidatePhoneSendOTP.as_view()),
    path('validate_otp/', ValidateOTP.as_view()),
    path('login/', Login.as_view()),
    path('registor/', Register.as_view()),
    path('edit_photo/',EditProfile.as_view()),
    path('profile/',Profileview.as_view()),
    path('api/', include('rest_framework.urls')),
    path('removeban/<int:pk>',  RemoveFromBanUser.as_view())

   
]
