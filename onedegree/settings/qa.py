# Django settings for formcms project.
from quanquan.settings.default import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT, mode=int('0755', 8))


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT, mode=int('0755', 8))
    

# since in py3 octal literals must now be specified with a leading "0o" or "0O" instead of "0"
FILE_UPLOAD_TEMP_DIR = os.path.join(BASE_DIR, 'tmp')
if not os.path.exists(FILE_UPLOAD_TEMP_DIR):
    os.makedirs(FILE_UPLOAD_TEMP_DIR, mode=int('0755', 8))
    
