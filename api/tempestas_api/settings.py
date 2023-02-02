"""
Django settings for tempestas_api project.

Generated by 'django-admin startproject' using Django 1.11.16.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SURFACE_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('SURFACE_DJANGO_DEBUG', False)

ALLOWED_HOSTS = ['*']

USE_X_FORWARDED_HOST = True

# Application definition

INSTALLED_APPS = [
    'material',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_celery_beat',
    'ckeditor',
    'wx',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'colorfield',
    'import_export',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tempestas_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wx.context_processors.get_surface_context',
                'wx.context_processors.get_user_wx_permissions',
            ],
        },
    },
]

WSGI_APPLICATION = 'tempestas_api.wsgi.application'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

DATABASES = {
    'default': {
        'ENGINE': os.getenv('SURFACE_DB_ENGINE'),
        'HOST': os.getenv('SURFACE_DB_HOST'),
        'PORT': os.getenv('SURFACE_DB_PORT'),
        'NAME': os.getenv('SURFACE_DB_NAME'),
        'USER': os.getenv('SURFACE_DB_USER'),
        'PASSWORD': os.getenv('SURFACE_DB_PASSWORD'),
    }
}

SURFACE_CONNECTION_STRING = "dbname={0} user={1} password={2} host={3}".format(os.getenv('SURFACE_DB_NAME'),
                                                                               os.getenv('SURFACE_DB_USER'),
                                                                               os.getenv('SURFACE_DB_PASSWORD'),
                                                                               os.getenv('SURFACE_DB_HOST'))

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = os.path.join('/data', 'media')

DOCUMENTS_URL = '/data/documents/'
DOCUMENTS_ROOT = os.path.join('/data/media', 'documents')

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 200,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1)
}

SURFACE_DATA_DIR = os.getenv('SURFACE_DATA_DIR', '/data')
SURFACE_BROKER_URL = os.getenv('SURFACE_BROKER_URL', 'redis://localhost:6379/0')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {name} {funcName} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'surface': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },

    }
}



CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'cache:11211',
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LRGS_EXECUTABLE_PATH = os.getenv('LRGS_EXECUTABLE_PATH')
LRGS_SERVER_HOST = os.getenv('LRGS_SERVER_HOST')
LRGS_SERVER_PORT = os.getenv('LRGS_SERVER_PORT')
LRGS_USER = os.getenv('LRGS_USER')
LRGS_PASSWORD = os.getenv('LRGS_PASSWORD')
LRGS_CS_FILE_PATH = os.getenv('LRGS_CS_FILE_PATH')
LRGS_MAX_INTERVAL = os.getenv('LRGS_MAX_INTERVAL')
LOGIN_REDIRECT_URL = os.getenv('LOGIN_REDIRECT_URL')
LOGOUT_REDIRECT_URL = os.getenv('LOGOUT_REDIRECT_URL')

ENTL_PRIMARY_SERVER_HOST = os.getenv('ENTL_PRIMARY_SERVER_HOST')
ENTL_PRIMARY_SERVER_PORT = int(os.getenv('ENTL_PRIMARY_SERVER_PORT'))
ENTL_SECONDARY_SERVER_HOST = os.getenv('ENTL_SECONDARY_SERVER_HOST')
ENTL_SECONDARY_SERVER_PORT = os.getenv('ENTL_SECONDARY_SERVER_PORT')
ENTL_PARTNER_ID = os.getenv('ENTL_PARTNER_ID')

TIMEZONE_NAME = os.getenv('TIMEZONE_NAME')
MISSING_VALUE = -99999
MISSING_VALUE_CODE = '/'
TIMEZONE_OFFSET = int(os.getenv('TIMEZONE_OFFSET'))

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 2 * 60 * 60
EXPORTED_DATA_CELERY_PATH = '/data/exported_data/'

INMET_HOURLY_DATA_URL = os.getenv('INMET_HOURLY_DATA_URL')
INMET_DAILY_DATA_BASE_PATH = os.getenv('INMET_DAILY_DATA_BASE_PATH')

MAP_LATITUDE = float(os.getenv('MAP_LATITUDE'))
MAP_LONGITUDE = float(os.getenv('MAP_LONGITUDE'))
MAP_ZOOM = int(os.getenv('MAP_ZOOM'))

SPATIAL_ANALYSIS_INITIAL_LATITUDE = float(os.getenv('SPATIAL_ANALYSIS_INITIAL_LATITUDE'))
SPATIAL_ANALYSIS_INITIAL_LONGITUDE = float(os.getenv('SPATIAL_ANALYSIS_INITIAL_LONGITUDE'))
SPATIAL_ANALYSIS_FINAL_LATITUDE = float(os.getenv('SPATIAL_ANALYSIS_FINAL_LATITUDE'))
SPATIAL_ANALYSIS_FINAL_LONGITUDE = float(os.getenv('SPATIAL_ANALYSIS_FINAL_LONGITUDE'))
SPATIAL_ANALYSIS_SHAPE_FILE_PATH = os.getenv('SPATIAL_ANALYSIS_SHAPE_FILE_PATH')

STATION_MAP_WIND_SPEED_ID = int(os.getenv('STATION_MAP_WIND_SPEED_ID'))
STATION_MAP_WIND_GUST_ID = int(os.getenv('STATION_MAP_WIND_GUST_ID'))
STATION_MAP_WIND_DIRECTION_ID = int(os.getenv('STATION_MAP_WIND_DIRECTION_ID'))
STATION_MAP_TEMP_MAX_ID = int(os.getenv('STATION_MAP_TEMP_MAX_ID'))
STATION_MAP_TEMP_MIN_ID = int(os.getenv('STATION_MAP_TEMP_MIN_ID'))
STATION_MAP_TEMP_AVG_ID = int(os.getenv('STATION_MAP_TEMP_AVG_ID'))
STATION_MAP_ATM_PRESSURE_ID = int(os.getenv('STATION_MAP_ATM_PRESSURE_ID'))
STATION_MAP_PRECIPITATION_ID = int(os.getenv('STATION_MAP_PRECIPITATION_ID'))
STATION_MAP_RELATIVE_HUMIDITY_ID = int(os.getenv('STATION_MAP_RELATIVE_HUMIDITY_ID'))
STATION_MAP_SOLAR_RADIATION_ID = int(os.getenv('STATION_MAP_SOLAR_RADIATION_ID'))
STATION_MAP_FILTER_WATERSHED = os.getenv('STATION_MAP_FILTER_WATERSHED', 0)
STATION_MAP_FILTER_REGION = os.getenv('STATION_MAP_FILTER_REGION', 0)
STATION_MAP_FILTER_PROFILE = os.getenv('STATION_MAP_FILTER_PROFILE', 0)
STATION_MAP_FILTER_COMMUNICATION = os.getenv('STATION_MAP_FILTER_COMMUNICATION', 0)

HYDROML_URL = 'http://hydroml-api:8000/en/web/api/predict/'
PGIA_REPORT_HOURS_AHEAD_TIME = 1