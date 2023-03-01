from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting
from urllib.parse import urljoin

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION

    # def _clean_name(self, name):
    #     return name

    # def _normalize_name(self, name):
    #     if not name.endswith('/'):
    #         name += "/"

    #     name = self.location + name
    #     return name


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION

    # def _clean_name(self, name):
    #     return name

    # def _normalize_name(self, name):
    #     if not name.endswith('/'):
    #         name += "/"

    #     name = self.location + name
    #     return name

    """
    GoogleCloudStorage extensions suitable for handing Django's
    Static and Media files.

    Requires following settings:
    MEDIA_URL, GS_MEDIA_BUCKET_NAME
    STATIC_URL, GS_STATIC_BUCKET_NAME

    In addition to
    https://django-storages.readthedocs.io/en/latest/backends/gcloud.html
    """



GoogleStatic = lambda: GoogleCloudStorage(location='static')
GoogleMedia = lambda: GoogleCloudStorage(location='media')