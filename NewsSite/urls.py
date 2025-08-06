from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('news/', include('news.urls')),
]

# Оборачиваем в i18n_patterns для поддержки интернационализации
urlpatterns += i18n_patterns(
    path('', RedirectView.as_view(pattern_name='news_list', permanent=False)),
)