from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views

# Создаем router для REST API
router = DefaultRouter()
router.register(r'api/news', views.NewsViewSet, basename='api-news')
router.register(r'api/articles', views.ArticleViewSet, basename='api-articles')
router.register(r'api/categories', views.CategoryViewSet, basename='api-categories')
router.register(r'api/comments', views.CommentViewSet, basename='api-comments')
router.register(r'api/users', views.UserViewSet, basename='api-users')

urlpatterns = [
    # Основные маршруты приложения
    path('', views.NewsListView.as_view(), name='news_list'),
    path('search/', views.NewsSearchView.as_view(), name='news_search'),
    path('create/', views.NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    path('<int:pk>/', views.NewsDetailViewWithComments.as_view(), name='news_detail'),
    path('<int:pk>/like/', views.news_like, name='news_like'),
    path('<int:pk>/dislike/', views.news_dislike, name='news_dislike'),

    # Маршруты для статей
    path('articles/', views.ArticlesListView.as_view(), name='articles_list'),
    path('articles/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('articles/<int:pk>/like/', views.article_like, name='article_like'),
    path('articles/<int:pk>/dislike/', views.article_dislike, name='article_dislike'),

    # Маршруты для пользователей
    path('become-author/', views.become_author, name='become_author'),
    path('subscriptions/', views.manage_subscriptions, name='manage_subscriptions'),
    path('unsubscribe/<int:category_id>/', views.unsubscribe, name='unsubscribe'),
    path('profile/', views.profile_view, name='profile'),

    # Утилиты
    path('set-timezone/', views.set_timezone, name='set_timezone'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),

    # Аутентификация
    path('accounts/logout/', views.custom_logout, name='account_logout'),
    path('accounts/', include('allauth.urls')),

    # REST API маршруты
    path('', include(router.urls)),
    path('api/subscriptions/', views.SubscriptionAPIView.as_view(), name='api_subscriptions'),
    path('api/profile/', views.ProfileAPIView.as_view(), name='api_profile'),
    path('api/become-author/', views.BecomeAuthorAPIView.as_view(), name='api_become_author'),

    # Аутентификация для API
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# Дополнительные маршруты для обработки ошибок
handler404 = 'news.views.custom_404'
handler500 = 'news.views.custom_500'