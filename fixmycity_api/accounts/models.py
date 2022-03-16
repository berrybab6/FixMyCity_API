from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import random
# from graphql_relay import to_global_id
from accounts.managers import UserManager


# def profile_pic_path(instance, filename):
#     rand_int = str(random.randint(0, 999999))
#     return 'user_{0}_profile_pic_{1}'.format(to_global_id('SuperAdminNode',instance.id), rand_int)


class SuperAdmin(AbstractBaseUser , PermissionsMixin):
    full_name = models.CharField(max_length=255 , null=False)
    password = models.CharField(max_length=255 , null=False)
    username = models.CharField(max_length=255 , null=False , unique=True)
    image = models.ImageField(upload_to='users' , null= True )
    created_at = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'username'
    objects = UserManager()
    
    
    def name(self):
        return self.full_name
    
   