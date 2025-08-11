import pytz
from django.utils import timezone

def timezone_context(request):
    return {
        'timezones': pytz.all_timezones,
        'current_timezone': request.session.get('django_timezone', 'UTC')
    }