from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import random
# from graphql_relay import to_global_id
from accounts.managers import UserManager

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import datetime

# def profile_pic_path(instance, filename):
#     rand_int = str(random.randint(0, 999999))
#     return 'user_{0}_profile_pic_{1}'.format(to_global_id('SuperAdminNode',instance.id), rand_int)


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, username, password=None,full_name=None, **extra_fields):
        """Create and save a User with the given username and password."""
        if not username:
            raise ValueError('The given username must be set')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.full_name=full_name
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, full_name=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password,full_name **extra_fields)

    def create_superuser(self, username, password=None, full_name=None,**extra_fields):
        """Create and save a SuperUser with the given username and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password,full_name, **extra_fields)



def upload_to(instance, filename):
    return '{datetime}{filename}'.format(datetime=datetime.now(), filename=filename)




# Create your models here.
class SuperAdmin(AbstractUser,PermissionsMixin):
    full_name = models.CharField(max_length=255 , null=False)
    username = models.CharField(max_length=255 , null=False , unique=True)
    image = models.ImageField(upload_to=upload_to , null= True )
    created_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'username'
    # objects = UserManager()
    
    
    objects = CustomUserManager()
    REQUIRED_FIELDS =[]

    def name(self):
        return self.full_name