from django.urls import path
from .views import ArticleListView, add_comment

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/<int:post_id>/comment/', add_comment, name='add_comment'),
]
