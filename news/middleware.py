from django.utils import timezone
import pytz
from django.utils.deprecation import MiddlewareMixin

class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if hasattr(request.user, 'userprofile'):
            tz = request.user.userprofile.timezone
            timezone.activate(pytz.timezone(tz))

class ThemeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'dark_mode' not in request.session:
            request.session['dark_mode'] = False