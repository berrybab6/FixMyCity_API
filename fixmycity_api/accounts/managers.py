from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    
    
    
    def create_normal_user(self, first_name, last_name=None,phone_number=None, **extra_fields):
        """Create and save a User with the given username and password."""
        if not first_name:
            raise ValueError('The given first_name must be set')
        if not last_name:
            raise ValueError('The given last_name must be set')
        if not phone_number:
            raise ValueError('The given phone_number must be set')
        
        user = self.model(first_name=first_name, last_name= last_name , phone_number= phone_number, **extra_fields)
        user.save(using=self._db)
        return user

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

