from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.core.cache import cache 
import datetime
from chess import settings

# Create your models here.

class Profile(models.Model):
    user = models .OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    created = models.DateTimeField(auto_now_add=True, null=True)
    last_activity = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f'{self.user.username} Profile'

    def last_seen(self):
        result = cache.get(f'seen_{self.user.username}')
        if not result:
            return self.last_activity
        return result

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                        seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False   
    
    class Meta:
        ordering = ['created']