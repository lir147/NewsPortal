from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path(_('news/'), include('news.urls')),  # Все новостные URLs будут здесь
    path('', include('news.urls')),  # Для редиректа с главной
    prefix_default_language=False
)