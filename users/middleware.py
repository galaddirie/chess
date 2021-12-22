import datetime
from django.core.cache import cache
from django.conf import settings
from .models import Profile

class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
    def __call__(self, request):
        current_user = request.user
        response = self.get_response(request)
        if request.user.is_authenticated:
            now = datetime.datetime.now()

            last_activity = cache.get(f'seen_{current_user.username}')
            
            # Profile.objects.filter(user=request.user) \
            #          .update(last_activity=now)
            if last_activity and last_activity < (now - datetime.timedelta(seconds = settings.USER_ONLINE_TIMEOUT)):
                cache.set(f'seen_{current_user.username}', now, timeout=settings.USER_LASTSEEN_TIMEOUT)
                # 
        
        return response
