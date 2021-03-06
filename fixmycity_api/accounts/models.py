
from http.client import ImproperConnectionState
from pickle import TRUE
from tokenize import blank_re
from django.conf import settings
from django.contrib.gis.db import models
from django.core.validators import RegexValidator

# Create your models here.
# from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import random
import jwt
from django.conf import settings
from datetime import datetime, timedelta
# from graphql_relay import to_global_id
# from accounts.managers import UserManager

# from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import datetime
from cloudinary.models import CloudinaryField



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
    """Define a model manager for User model with no email field."""

    def _create_user(self, email,password=None,role=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        # if not role: 
            # raise ValueError('The given Role must be set')

        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        # user.full_name=full_name
        ro = Role.objects.get(id=role)
        
        user.roles = ro
        user.save(using=self._db)
        # user.roles.set(ro)
        return user

    def create_user(self,email, password=None,**extra_fields):
        # extra_fields.setdefault('roles',3)
        # if extra_fields.get('roles') != 3:
            # raise ValueError('User must have role=3.')

        return self._create_user(email, password,role=3, **extra_fields)

    def create_sectoradmin(self, email, password=None,**extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('main_sector', True)
        # extra_fields.setdefault('roles', 2)

        if extra_fields.get('main_sector') is not True:
            raise ValueError('Sector Admin must have main_sector=True.')
        # if extra_fields.get('roles') != 2:
            # raise ValueError('Sector Admin must have role=2.')

        return self._create_user(email, password, role=2,**extra_fields)

    def create_superuser(self, email, password=None,**extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('staff', True)
        extra_fields.setdefault('active',True)
        # extra_fields.setdefault('roles', 1)
        # if extra_fields.get('roles') != 1:
            # raise ValueError('Super Admin must have role=1.')
        # ro = Role.objects.get(id=1) 
        return self._create_user(email, password,role=1,**extra_fields)


def upload_to(instance, filename):
    return '{datetime}{filename}'.format(datetime=datetime.now(), filename=filename)

    



class Sector(models.Model):

    TELE = 1
    WATER_AND_SEWAGE = 2
    ROADS_AUTHORITY = 3
    ELPA = 4
    SECTOR_TYPE = ((TELE,'tele'), (WATER_AND_SEWAGE, 'water_and_sewage'), (ROADS_AUTHORITY, 'roads_authority'), (ELPA, 'elpa'))       
    sector_type = models.PositiveSmallIntegerField(
        choices=SECTOR_TYPE, null=True)
    district_name = models.CharField(unique=True,max_length=150)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=150, unique=True)
    location = models.PointField(null=True, blank=True,)
    address = models.CharField(max_length=255 , null=True)
    main_sector = models.BooleanField(default=False)
    sector_logo = models.ImageField(upload_to="logo", blank=True, null = True)
    def __str__(self):
        return self.district_name

    

class User(AbstractBaseUser, PermissionsMixin):
    roles = models.ForeignKey(Role, on_delete=models.CASCADE,db_column='rolesId', null=True)
    id = models.AutoField(primary_key=True)
    # username = models.CharField(max_length=255 , null=False , unique=True)
    created_at = models.DateTimeField(auto_now=True)
    staff = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    main_sector = models.BooleanField(default=False)
    email = models.EmailField(max_length=150, unique=True , null=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE,related_name="sector", null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number     = models.CharField( max_length=15, unique=True , null=True)
    first_name       = models.CharField(max_length = 255, null = True)
    last_name        = models.CharField(max_length = 255, null = True)
    ProfileImage     = CloudinaryField('image' , null=True , blank= True)
    # admin = models.BooleanField(default=False)
    count_strike = models.IntegerField(default=0)
    is_banned = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    # objects = UserManager()
    REQUIRED_FIELDS =[]

    
    objects = CustomUserManager()
    def name(self):
        return str(self.first_name)
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
        return str(self.id)
    
    # @property
    # def token(self):
    #     print(self.sector.district_name)
    #     print(self.role)
    #     print("here")
    #     print(self.sector)
    #     if self.role == 2:
    #         token = jwt.encode({'user_id':self.id , 'sector': self.sector.district_name ,'exp': datetime.utcnow() + timedelta(hours=24) }, settings.SECRET_KEY, algorithm='HS256')
    #         print(token)
    #         return token
    
    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         username = self.username
    #         username_exists = True
    #         counter = 1
    #         self.username = username
    #         while username_exists:
    #             try:
    #                 username_exists = User.objects.get(username=username)
    #                 if username_exists:
    #                     username = self.username + '_' + str(counter)
    #                     counter += 1
    #             except User.DoesNotExist:
    #                 self.username = username
    #                 break
    #     super(User, self).save(*args, **kwargs)

    class Meta:
        abstract = False

    
class PhoneOTP(models.Model):
    phone_regex        = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+9xxxxxxxxxx'. Up to 10 digits allowed.")
    phone_number       = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    otp                = models.CharField(max_length = 9, blank = True, null= True)
    count              = models.IntegerField(default = 0, help_text = 'Number of otp sent')
    logged             = models.BooleanField(default = False, help_text = 'If otp verification got successful')
    

    def __str__(self):
        return str(self.phone_number) + ' is sent ' + str(self.otp)
    
    
    


# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

#     email_plaintext_message = "{}?token={}".format('http://127.0.0.1:3000/newpassword', reset_password_token.key)
   
#     send_mail(
#         # title:
#         "Password Reset for {title}".format(title="Some website title"),
#         # message:
#         email_plaintext_message,
#         # from:
#         "wubshetgenetu21@gmail.com",
#         # to:
#         [reset_password_token.user.email]
#     )

   

