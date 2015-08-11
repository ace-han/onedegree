# Django settings for core project.
from onedegree.settings.default import *

DEBUG = True
TEMPLATE_DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'onedegree',                      # Or path to database file if using sqlite3.
        'USER': 'onedegree',                      # Not used with sqlite3.
        'PASSWORD': 'onedegree',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',
        'OPTIONS': {
            # options could be found http://mysql-python.sourceforge.net/MySQLdb.html
            # pre db setup scripts, plz see to freq_scripts.txt 
            'init_command': "SET storage_engine=INNODB, time_zone='%s'" % TIME_ZONE,
            'charset': 'utf8',
        }
    }
}

#'''
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT, mode=int('0755', 8))


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT, mode=int('0755', 8))
    

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

# since in py3 octal literals must now be specified with a leading "0o" or "0O" instead of "0"
FILE_UPLOAD_TEMP_DIR = os.path.join(BASE_DIR, 'tmp', 'uploads')
if not os.path.exists(FILE_UPLOAD_TEMP_DIR):
    os.makedirs(FILE_UPLOAD_TEMP_DIR, mode=int('0755', 8))
    
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'tmp', 'emails')
if not os.path.exists(EMAIL_FILE_PATH):
    os.makedirs(EMAIL_FILE_PATH, mode=int('0755', 8))
    
update_log_level(LOGGING, 'DEBUG')