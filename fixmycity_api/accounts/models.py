from pickle import TRUE
from django.conf import settings
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



class Role(models.Model):
    SUPER_ADMIN = 1
    CUSTOM_USER = 3

    SECTOR_ADMIN = 2
    STAFF = 4
    ROLE_CHOICES = (
        (SUPER_ADMIN, 'super_admin'),
        (CUSTOM_USER, 'custom_user'),
        (SECTOR_ADMIN, 'sector_admin'),

      
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return str(self.get_id_display())

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, username,password=None,full_name=None,role=None, **extra_fields):
        """Create and save a User with the given username and password."""
        if not username:
            raise ValueError('The given username must be set')
        # if not role: 
            # raise ValueError('The given Role must be set')

        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.full_name=full_name
        ro = Role.objects.get(id=role)
        
        user.roles = ro
        user.save(using=self._db)
        # user.roles.set(ro)
        return user

    def create_user(self,username, password=None, full_name=None,**extra_fields):
        # extra_fields.setdefault('roles',3)
        # if extra_fields.get('roles') != 3:
            # raise ValueError('User must have role=3.')

        return self._create_user(username, password,full_name,role=3, **extra_fields)

    def create_sectoradmin(self, username, password=None, full_name=None,**extra_fields):
        """Create and save a SuperUser with the given username and password."""
        extra_fields.setdefault('main_sector', True)
        # extra_fields.setdefault('roles', 2)

        if extra_fields.get('main_sector') is not True:
            raise ValueError('Sector Admin must have main_sector=True.')
        # if extra_fields.get('roles') != 2:
            # raise ValueError('Sector Admin must have role=2.')

        return self._create_user(username, password,full_name, role=2,**extra_fields)

    def create_superuser(self, username, password=None, full_name=None,**extra_fields):
        """Create and save a SuperUser with the given username and password."""
        extra_fields.setdefault('staff', True)
        extra_fields.setdefault('active',True)
        # extra_fields.setdefault('roles', 1)
        # if extra_fields.get('roles') != 1:
            # raise ValueError('Super Admin must have role=1.')
        # ro = Role.objects.get(id=1) 
        return self._create_user(username, password,full_name,role=1,**extra_fields)


def upload_to(instance, filename):
    return '{datetime}{filename}'.format(datetime=datetime.now(), filename=filename)
class User(AbstractBaseUser, PermissionsMixin):
    roles = models.ForeignKey(Role, on_delete=models.CASCADE,db_column='rolesId')

# class Admins(models.Model):
    # roles = models.ManyToManyField(Role)
    id = models.AutoField(primary_key=True)

    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=255 , null=True)
    username = models.CharField(max_length=255 , null=False , unique=True)
    image = models.ImageField(upload_to=upload_to , null= True, blank=True )
    created_at = models.DateTimeField(auto_now=True)
    staff = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    # admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'username'
    # objects = UserManager()
    REQUIRED_FIELDS =[]

    
    objects = CustomUserManager()
    def name(self):
        return str(self.full_name)
    def rolem(self):
        return self.roles
    # class Meta:
        # abstract = True
    @property
    def role(self):
        return self.roles.id
    def has_module_perms(self, app_label):
        is_admin = False
        if self.role==1:
            is_admin=True

        return is_admin
    def has_perm(self, perm, obj=None):
        is_admin = False
        if self.role ==1:
            is_admin=True
        return is_admin

    @property
    def is_staff(self):
        return self.staff
    @property
    def is_active(self):
        return self.active
    def __str__(self):
        return str(self.username) if self.username else ''

    class Meta:
        abstract = False
# Create your models here.
class SectorAdmin(User):
    sector_user = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)
    email = models.EmailField(max_length=100, null=False)
    main_sector = models.BooleanField(default=False)
    @property
    def is_main_sector(self):
        return self.main_sector
    objects = CustomUserManager()

   