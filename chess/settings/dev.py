from .base import *

SECRET_KEY = 'django-insecure-q2_(obwdl5tci50+1md$uxp_l5_q(3pt1ui!8hu@-fm8mm=7-@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
