from django.utils import timezone
import pytz
from django.conf import settings

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request.user, 'userprofile') and hasattr(request.user.userprofile, 'timezone'):
            timezone.activate(pytz.timezone(request.user.userprofile.timezone))
        elif 'django_timezone' in request.session:
            timezone.activate(pytz.timezone(request.session['django_timezone']))
        return self.get_response(request)

class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'theme' not in request.session:
            request.session['theme'] = settings.DEFAULT_THEME
        return self.get_response(request)