from django.urls import path
from .views import (
    article_like, article_dislike,
    NewsListView, NewsSearchView, NewsCreateView, NewsUpdateView, NewsDeleteView, NewsDetailView,
    ArticlesListView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView
)

urlpatterns = [

    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/search/', NewsSearchView.as_view(), name='news_search'),
    path('news/_create_/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/_edit_/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/_delete_/', NewsDeleteView.as_view(), name='news_delete'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),


    path('articles/', ArticlesListView.as_view(), name='articles_list'),
    path('articles/_create_/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/_edit_/', ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/_delete_/', ArticleDeleteView.as_view(), name='article_delete'),
    path('articles/<int:pk>/', NewsDetailView.as_view(), name='article_detail'),  # возможно, будет лучше сделать отдельный DetailView


    path('articles/<int:pk>/like/', article_like, name='article_like'),
    path('articles/<int:pk>/dislike/', article_dislike, name='article_dislike'),
]