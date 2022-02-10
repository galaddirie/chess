from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .models import Profile
import uuid
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    player_id = models.UUIDField(unique=True,
                                 primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(default='default.png',
                              null=True, upload_to='profile_pics')
    created = models.DateTimeField(auto_now_add=True, null=True)
    last_activity = models.DateTimeField(auto_now=True)
    session_id = models.CharField(max_length=32, null=True, blank=True)
    sanitized_name = models.CharField(
        max_length=150, null=True, blank=True)

    def __str__(self) -> str:
        if self.user:
            return f'{self.user.username} Profile'
        return f'Anonymous@{self.session_id} Profile'

    @staticmethod
    def get_profile(name: str) -> Profile:
        """
        Returns a Profile object with the name given
        """

        profile = Profile.objects.get(sanitized_name=name)
        return profile

    def is_auth_user(self):
        return self.user != None

    def save(self, *args, **kwargs):

        # if not self.sanitized_name:
        try:
            name = self.user.username.lower()
            name = ''.join(name.split())
            self.sanitized_name = name
        except AttributeError:
            name = self.session_id.lower()
            name = ''.join(name.split())
            self.sanitized_name = name
        super(Profile, self).save(*args, **kwargs)

    class Meta:
        ordering = ['created']
