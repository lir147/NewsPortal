import os
from django.core.asgi import get_asgi_application
from django.utils.translation import gettext_lazy as _

WELCOME = _('Добро пожаловать в NewsSite!')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsSite.settings')

application = get_asgi_application()