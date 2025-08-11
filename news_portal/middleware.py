from django.utils import timezone
import pytz

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request.user, 'userprofile'):
            timezone.activate(pytz.timezone(request.user.userprofile.timezone))
        return self.get_response(request)