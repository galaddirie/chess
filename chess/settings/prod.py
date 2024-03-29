from .base import *
import json
import django_on_heroku
from decouple import config
from google.oauth2 import service_account

SECRET_KEY =' os.environ.get("SECRET_KEY")'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'chess-stream.herokuapp.com'
]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True


# AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
# AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
# AWS_S3_SIGNATURE_VERSION = 's3v4'
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400'
# }
# AWS_LOCATION = 'static/'
# AWS_QUERYSTRING_AUTH = False
# AWS_HEADERS = {
#     'Access-Control-Allow-Origin': '*'
# }

# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
# STATICFILES_STORAGE = "custom_storages.StaticStorage

GS_BUCKET_NAME = os.environ.get("GS_BUCKET_NAME")
GS_PROJECT_ID = os.environ.get("GS_PROJECT_ID")
json_str = os.environ.get('GOOGLE_CREDENTIALS')
json_data = json.loads(json_str)
json_data['private_key'] = json_data['private_key'].replace('\\n', '\n')
GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
    json_data
)
GS_DEFAULT_ACL = "publicRead"

STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.GoogleStatic'

# DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'custom_storages.GoogleMedia'

# Heroku Logging
DEBUG_PROPAGATE_EXCEPTIONS = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}
# # Heroku settings
django_on_heroku.settings(locals(), staticfiles=False)
del DATABASES['default']['OPTIONS']['sslmode']
