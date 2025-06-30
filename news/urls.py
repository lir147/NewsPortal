from django.urls import path
from .views import NewsListView, NewsSearchView, NewsCreateView, NewsUpdateView, NewsDeleteView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView

urlpatterns = [
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/search/', NewsSearchView.as_view(), name='news_search'),

    path('news/_create_/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/_edit_/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/_delete_/', NewsDeleteView.as_view(), name='news_delete'),

    path('articles/_create_/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/_edit_/', ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/_delete_/', ArticleDeleteView.as_view(), name='article_delete'),
]