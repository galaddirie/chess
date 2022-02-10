from .base import *

SECRET_KEY = '123456789'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
