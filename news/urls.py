from django.urls import path
from django.utils.translation import gettext_lazy as _
from . import views

urlpatterns = [
    path('accounts/logout/', views.custom_logout, name='account_logout'),
    path('', views.NewsListView.as_view(), name='news_list'),
    path('search/', views.NewsSearchView.as_view(), name='news_search'),
    path('create/', views.NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    path('<int:pk>/', views.NewsDetailViewWithComments.as_view(), name='news_detail'),
    path('<int:pk>/like/', views.news_like, name='news_like'),
    path('<int:pk>/dislike/', views.news_dislike, name='news_dislike'),

    path('articles/', views.ArticlesListView.as_view(), name='articles_list'),
    path('articles/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('articles/<int:pk>/like/', views.article_like, name='article_like'),
    path('articles/<int:pk>/dislike/', views.article_dislike, name='article_dislike'),

    path('become-author/', views.become_author, name='become_author'),
    path('subscriptions/', views.manage_subscriptions, name='manage_subscriptions'),
    path('unsubscribe/<int:category_id>/', views.unsubscribe, name='unsubscribe'),
    path('profile/', views.profile_view, name='profile'),

    path('set-timezone/', views.set_timezone, name='set_timezone'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
]