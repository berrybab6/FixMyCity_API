from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from accounts import managers




class User(AbstractBaseUser):
    phone_regex      = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+9xxxxxxxxx'. Up to 10 digits allowed.")
    phone_number     = models.CharField(validators=[phone_regex], max_length=10, unique=True)
    first_name       = models.CharField(max_length = 255, null = True)
    last_name        = models.CharField(max_length = 255, null = True)
    ProfileUrl       = models.CharField(max_length = 255  , null=True , blank=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = managers.CustomUserManager()

    def __str__(self):
        return self.phone_number
    
    
    
class PhoneOTP(models.Model):
    phone_regex        = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+9xxxxxxxxxx'. Up to 10 digits allowed.")
    phone_number       = models.CharField(validators=[phone_regex], max_length=10, unique=True)
    otp                = models.CharField(max_length = 9, blank = True, null= True)
    count              = models.IntegerField(default = 0, help_text = 'Number of otp sent')
    logged             = models.BooleanField(default = False, help_text = 'If otp verification got successful')
    

    def __str__(self):
        return str(self.phone_number) + ' is sent ' + str(self.otp)

   

