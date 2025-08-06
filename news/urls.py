from django.urls import path
from .views import (
    article_like, article_dislike,
    NewsListView, NewsSearchView, NewsCreateView, NewsUpdateView, NewsDeleteView,
    ArticlesListView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView,
    news_like, news_dislike, NewsDetailViewWithComments, ArticleDetailView,
    register, become_author, manage_subscriptions, profile_view, unsubscribe
)

urlpatterns = [
    path('accounts/register/', register, name='register'),
    # Новости
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/search/', NewsSearchView.as_view(), name='news_search'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('news/<int:pk>/', NewsDetailViewWithComments.as_view(), name='news_detail'),
    path('news/<int:pk>/like/', news_like, name='news_like'),
    path('news/<int:pk>/dislike/', news_dislike, name='news_dislike'),

    # Стать автором
    path('become-author/', become_author, name='become_author'),

    # Подписки на категории
    path('subscriptions/', manage_subscriptions, name='manage_subscriptions'),
    path('unsubscribe/<int:category_id>/', unsubscribe, name='unsubscribe'),

    # Профиль
    path('profile/', profile_view, name='profile'),

    # Статьи
    path('articles/', ArticlesListView.as_view(), name='articles_list'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/<int:pk>/like/', article_like, name='article_like'),
    path('articles/<int:pk>/dislike/', article_dislike, name='article_dislike'),
]