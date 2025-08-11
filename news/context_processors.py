import pytz
from django.conf import settings

def timezone_context(request):
    """Контекст-процессор для работы с часовыми поясами"""
    return {
        'current_timezone': request.session.get('django_timezone', settings.TIME_ZONE),
        'timezones': pytz.all_timezones,
    }

def theme_context(request):
    """Контекст-процессор для работы с темами оформления"""
    return {
        'current_theme': request.session.get('theme', settings.DEFAULT_THEME),
        'available_themes': ['light', 'dark'],
    }