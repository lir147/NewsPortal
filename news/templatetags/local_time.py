from django import template
from django.utils import timezone
import pytz

register = template.Library()

@register.filter
def localize_time(value, timezone_str):
    tz = pytz.timezone(timezone_str)
    return value.astimezone(tz)