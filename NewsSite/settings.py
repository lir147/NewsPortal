import os
from pathlib import Path
from celery.schedules import crontab
import pytz


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-(jhr0@l$f9lfi=hhmf4%c+ty(tx1h2g_&vw$v#nmhlry&f6hxr'
DEBUG = True
ALLOWED_HOSTS = ['*']

# Приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    # Сторонние приложения
    'django_apscheduler',
    'django_celery_beat',
    'django_filters',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.yandex',
    'modeltranslation',

    # Локальные приложения
    'news.apps.NewsConfig',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'news.middleware.TimezoneMiddleware',
    'news.middleware.ThemeMiddleware',
]

ROOT_URLCONF = 'NewsSite.urls'

# Шаблоны
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'news.context_processors.timezone_context',
                'news.context_processors.theme_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'NewsSite.wsgi.application'

# База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Валидация паролей
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Интернационализация
LANGUAGE_CODE = 'ru'
LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Русский'),
]
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [BASE_DIR / 'locale']

# Статические файлы
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Аутентификация
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = 'news_list'
LOGOUT_REDIRECT_URL = 'account_login'

# Настройки allauth
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'your-email@yandex.ru'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'News Portal <your-email@yandex.ru>'
SITE_URL = 'http://127.0.0.1:8000'

# Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'

CELERY_BEAT_SCHEDULE = {
    'weekly-newsletter-every-monday-8am': {
        'task': 'news.tasks.weekly_newsletter',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),
    },
    'auto-switch-theme': {
        'task': 'news.tasks.auto_switch_theme',
        'schedule': crontab(minute=0, hour='*/1'),
    },
}

# Кэширование
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    },
    'timezone': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'timezone-cache',
    }
}

# Сессии
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_COOKIE_AGE = 1209600  # 2 недели

# Безопасность
CSRF_FAILURE_VIEW = 'news.views.csrf_failure'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'


LOGGING = {
'version': 1,
'disable_existing_loggers': False,
'filters': {
'require_debug_true': {
'()': 'django.utils.log.RequireDebugTrue',
},
'require_debug_false': {
'()': 'django.utils.log.RequireDebugFalse',
},
},
'formatters': {
'console_debug': {
'format': '{asctime} {levelname} {message}',
'style': '{',
'datefmt': '%Y-%m-%d %H:%M:%S',
},
'console_warning_or_above': {
'format': '{asctime} {levelname} {pathname} {message}',
'style': '{',
'datefmt': '%Y-%m-%d %H:%M:%S',
},
'console_error_critical': {
'format': '{asctime} {levelname} {pathname} {message}\n{exc_text}',
'style': '{',
'datefmt': '%Y-%m-%d %H:%M:%S',
},
'general_file': {
'format': '{asctime} {levelname} {module} {message}',
'style': '{',
'datefmt': '%Y-%m-%d %H:%M:%S',
},
'errors_file': {
'format': '{asctime} {levelname} {message} {pathname}\n{exc_text}',
'style': '{',
'datefmt': '%Y-%m-%d %H:%M:%S',
},
'security_file': {
'format': '{asctime} {levelname} {module} {message}',
'style': '{',
'datefmt': '%Y-%m-%d %H:%M:%S',
},
'mail': {
'format': '{asctime} {levelname} {message} {pathname}',
'style': '{',
'datefmt': '%Y-%m-%d %H:%M:%S',
},
},
'handlers': {
'console_debug': {
'level': 'DEBUG',
'filters': ['require_debug_true'],
'class': 'logging.StreamHandler',
'formatter': 'console_debug',
},
'console_warning_or_above': {
'level': 'WARNING',
'filters': ['require_debug_true'],
'class': 'logging.StreamHandler',
'formatter': 'console_warning_or_above',
},
'console_error_critical': {
'level': 'ERROR',
'filters': ['require_debug_true'],
'class': 'logging.StreamHandler',
'formatter': 'console_error_critical',
},
'general_file': {
'level': 'INFO',
'filters': ['require_debug_false'],
'class': 'logging.FileHandler',
'filename': 'general.log',
'formatter': 'general_file',
'encoding': 'utf8',
},
'errors_file': {
'level': 'ERROR',
'class': 'logging.FileHandler',
'filename': 'errors.log',
'formatter': 'errors_file',
'encoding': 'utf8',
},
'security_file': {
'level': 'DEBUG',
'class': 'logging.FileHandler',
'filename': 'security.log',
'formatter': 'security_file',
'encoding': 'utf8',
},
'mail_admins': {
'level': 'ERROR',
'filters': ['require_debug_false'],
'class': 'django.utils.log.AdminEmailHandler',
'include_html': False,
},
},
'loggers': {
'django': {
'handlers': ['console_debug', 'console_warning_or_above', 'console_error_critical', 'general_file'],
'level': 'DEBUG',
'propagate': True,
},
'django.request': {
'handlers': ['errors_file', 'mail_admins'],
'level': 'ERROR',
'propagate': False,
},
'django.server': {
'handlers': ['errors_file', 'mail_admins'],
'level': 'ERROR',
'propagate': False,
},
'django.template': {
'handlers': ['errors_file'],
'level': 'ERROR',
'propagate': False,
},
'django.db.backends': {
'handlers': ['errors_file'],
'level': 'ERROR',
'propagate': False,
},
'django.security': {
'handlers': ['security_file'],
'level': 'DEBUG',
'propagate': False,
},
},
}

DEFAULT_THEME = 'light'  # или 'dark'
THEME_COOKIE_NAME = 'newsportal_theme'
THEME_COOKIE_AGE = 30 * 24 * 60 * 60
# Модель перевода
MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'en'