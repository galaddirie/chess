from .base import *

SECRET_KEY = '123456789'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# development docker postgres database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        "HOST": "db",
        "PORT": 5432,
        "USER": "postgres",
        "PASSWORD": "postgres",
    }
}


STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
