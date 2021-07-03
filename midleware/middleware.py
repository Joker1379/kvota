import datetime
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin 

# Number of seconds that we will keep track of inactive users:
USER_STATUS_TIMEOUT = 60*60*24*7

class ActiveUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_user = request.user
        if request.user.is_authenticated:
            now = datetime.datetime.now()
            cache.set('seen_'+current_user.username, now, USER_STATUS_TIMEOUT)