from django.urls import path
from .views import ArticleListView, add_comment, news_list, news_detail

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('news/', news_list, name='news_list'),
    path('news/<int:news_id>/', news_detail, name='news_detail'),
]