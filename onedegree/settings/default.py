"""
Django settings for onedegree project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import datetime
import os
from os.path import dirname

from django.utils.translation import ugettext_lazy as _


BASE_DIR = os.path.realpath(dirname(dirname(dirname(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bu&p26myrt*eak6sqj6xu09ci%2n27_15@7hy6x6rev4yn&xap'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    '.madeinace.com',
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.admin', # since it will be ng-admin
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'social.apps.django_app.default',
    'pytz',
    'rest_framework',
    'taggit', # getting rid of django 1.9 warning. DB table like taggit_xxx are not necessary
    
    'onedegree',
    'admin',
    'tag',
    'authx',
    'account',
    'friend',
    
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'onedegree.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                'django.core.context_processors.csrf',
                "django.core.context_processors.tz",
                
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'onedegree.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
# monkey patch for pymysql as db level

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass 


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 60*1,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, '..', 'onedegree-media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'onedegree', 'static').replace('\\', '/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
PROJECT_LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(PROJECT_LOG_DIR):
    os.makedirs(PROJECT_LOG_DIR)
    
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        }
        # Log to a file that can be rotated by logrotate
        ,'file': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(PROJECT_LOG_DIR, 'app.log'),
            'formatter': 'verbose'
        }
        ,'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        }
        ,'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
        ,'db_debug': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(PROJECT_LOG_DIR, 'db.log'),
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.request': {
            # 'handlers': ['file', 'mail_admins'],
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
     
        'django.db.backends':{
            'handlers': ['db_debug'],
            'level': 'ERROR',
            'propagate': True,
        }

    }
}

# since in py3 octal literals must now be specified with a leading "0o" or "0O" instead of "0"
FILE_UPLOAD_PERMISSIONS = int('0644', 8)
FILE_UPLOAD_MAX_MEMORY_SIZE = 4*1024*1024
FILE_UPLOAD_TEMP_DIR = os.path.join(BASE_DIR, 'tmp')

LANGUAGES = (
    ## Customize this
    ('en', _('English')),
    ('zh-cn', _('Simplified Chinese')),
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

"""
Provide a function to update the LOGGING level in each environment's setting
"""
def update_log_level(logger, level):
    level_key = 'level'
    if type(logger) is dict:
        for key in logger:
            if key == level_key:
                logger[key] = level
            else:
                update_log_level(logger[key], level)

# add Django 1.7 DB migration support for easy_thumbnails instead of South
# since Django 1.7 has its own `python manage.py migrations` for database migrations
# which conflicts with South in the same package place `migration`
# South could not understand the instruction generated by Django 1.7
# plz refer to http://treyhunner.com/2014/03/migrating-to-django-1-dot-7
SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations',
}

AUTH_USER_MODEL = 'authx.User'

# ONLY left the default account backend here for a later extend point
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL

# In case you need a custom namespace, this setting is also needed:
SOCIAL_AUTH_URL_NAMESPACE = 'social'
# For those that prefer slugged usernames, 
# the get_username pipeline can apply a slug transformation (code borrowed from Django project) 
# by defining this setting to True. 
# The feature is disabled by default to to not force this option to all projects.
# SOCIAL_AUTH_SLUGIFY_USERNAMES = True

# by the nature of the application which depends on the existence of a user model, 
# it’s easy to fall in a recursive import ordering making the application fail to load. 
# This happens because the admin module will build a set of fields to populate the search_fields property 
# to search for related users in the administration UI, 
# but this requires the user model to be retrieved which might not be defined at that time.
# SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']

# SOCIAL_AUTH_USERNAME_FORM_HTML = 'username_signup.html'

# JWT config
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny', # for the time being only
    ), 
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    # this should align the same as django GenericListView paginate_by, page_size mechanism
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',
                                'rest_framework.filters.SearchFilter',
                                'rest_framework.filters.OrderingFilter', ), 
    'SEARCH_PARAM': 'q',
    'ORDERING_PARAM': 'ordering', 
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    #'PAGE_QUERY_PARAM': 'page', # sadly no this config, 'page' already is the default query param for this PageNumberPagination
    'PAGINATE_BY_PARAM': 'page_size',
    
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=14),
    'JWT_PAYLOAD_HANDLER': 'auth.utils.jwt_payload_handler',
}

