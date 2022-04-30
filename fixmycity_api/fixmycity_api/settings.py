"""
Django settings for fixmycity_api project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# import dj_database_url


import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
 
MODELS = os.path.join(BASE_DIR, 'ml/models')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-cj=gnk0t6yh8um+^&(0+2+zpjp=9(1ye@twg*)6179m4h&eap4'
# SECRET_KEY = os.getenv("SECRET_KEY","fixmycitysecretkey")
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY', default='foo')

DEBUG = int(os.environ.get('DEBUG', default=1))

# ALLOWED_HOSTS = ['fixmycity.ga','fixmycity-api.herokuapp.com','127.0.0.1','localhost']
ALLOWED_HOSTS=['*']
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'django.contrib.gis',
    'corsheaders',
    'cloudinary',
    'cloudinary_storage',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    # 'accounts.apps.AccountsConfig',
    'accounts',
    'users',
    'reports',
    'announcment'
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK  = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'fixmycity_api.jwt.JwtAuthentication',
       
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        
        
        #  'rest_framework.permissions.IsAuthenticated', # make all endpoints private
    ),
     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
     'PAGE_SIZE': 10
        
        
        
       
    
    
    }
AUTHENTICATION_BACKENDS = [
    # Application custom auth backend
    'fixmycity_api.auth.AuthentificationBackend',
]

ROOT_URLCONF = 'fixmycity_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': 'accounts/verify_email.html',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fixmycity_api.wsgi.application'
AUTH_USER_MODEL = 'accounts.User'



# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'fixmycity',
        'USER': 'postgres',
        'PASSWORD': 'test123',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3002",
    "https://fixmycity-24.herokuapp.com",
    "https://fixmycity5-24.herokuapp.com",
    "http://localhost:3000",
    "http://192.168.8.106:3000",
    'https://7677-197-156-86-169.ngrok.io',
    'https://ef71-197-156-86-181.ngrok.io'
]
CSRF_TRUSTED_ORIGINS = [
    "https://2a06-197-156-86-124.ngrok.io",
    "https://294a-197-156-77-127.ngrok.io",
    "http://localhost:3002",
    'https://fixmycity-24.herokuapp.com',
    "https://fixmycity5-24.herokuapp.com",
     "http://localhost:3000",
    "http://192.168.8.106:3000",
    'https://7677-197-156-86-169.ngrok.io',
    'https://ef71-197-156-86-181.ngrok.io'
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# DATABASE_URL = os.environ.get('DATABASE_URL')
# db_from_env = dj_database_url.config(default=DATABASE_URL, conn_max_age=500, ssl_require=True)
# DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# Cloudinary stuff
from decouple import config

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': "fixmy",
    'API_KEY': "643632981747267",
    'API_SECRET': "Td25NOCD3ztR2wjDx475BeQdh_w",
}

cloudinary.config(
    cloud_name="shetechs",
    api_key="171174673812633",
    api_secret="1Adci2An4RTqgFakBpoF5vMz63I"
)

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}


# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': config('CLOUD_NAME', default=""),
#     'API_KEY': config('API_KEY', default=""),
#     'API_SECRET': config('API_SECRET', default=""),
# }
# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': os.environ.get("CLOUD_NAME",default="foo1"),
#     'API_KEY': os.environ.get('API_KEY', default="foo2"),
#     'API_SECRET': os.environ.get('API_SECRET', default="foo3"),
# }

# os.environ.get("Key")
MEDIA_URL = '/media/'
MEDIA_ROOT = 'media'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# STATIC_ROOT = BASE_DIR / 'staticfiles'

# Extra places for collectstatic to find static files.
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Extra places for collectstatic to find static files.
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )
# STATIC_ROOT = 'static/'
# STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
    'TOKEN_TYPE_CLAIM': 'access'
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'wubshetgenetu21@gmail.com'
EMAIL_HOST_PASSWORD = 'fslgeuvbslfhakax'