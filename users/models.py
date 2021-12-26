import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.core.cache import cache 
import datetime, pytz
from chess import settings

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    player_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(default='default.png', null=True, upload_to='profile_pics')
    created = models.DateTimeField(auto_now_add=True, null=True)
    last_activity = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self) -> str:
        if self.user:
            return f'{self.user.username} Profile'
        return  f'Anonymous@{self.session_id} Profile'

    def last_seen(self):
        result = cache.get(f'seen_{self.user.username}')
        # if not result:
        #     return self.last_activity
        return result

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            now = pytz.utc.localize(now)
            last = (self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT))
            last = pytz.utc.localize(last)
            return now > last      
        else:
            return False   
    

    class Meta:
        ordering = ['created']