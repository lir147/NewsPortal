from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.utils import timezone
from django_filters.views import FilterView
import django_filters
from django import forms
from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.utils.dateparse import parse_date

from .models import Post, Comment

# Лайки/дизлайки для статей
@login_required
@require_POST
def article_like(request, pk):
    article = get_object_or_404(Post, pk=pk, post_type='article')
    article.rating += 1
    article.save()
    return redirect('article_detail', pk=pk)

@login_required
@require_POST
def article_dislike(request, pk):
    article = get_object_or_404(Post, pk=pk, post_type='article')
    article.rating -= 1
    article.save()
    return redirect('article_detail', pk=pk)

# Форма для создания/редактирования поста
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['post_type', 'created_at']

# Фильтр для поиска новостей
class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Название')
    author__user__username = django_filters.CharFilter(field_name='author__user__username', lookup_expr='icontains', label='Автор')
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', label='После даты', widget=forms.DateInput(attrs={'type':'date'}))

    class Meta:
        model = Post
        fields = ['title', 'author__user__username', 'created_at']

# Список новостей с пагинацией
class NewsListView(ListView):
    model = Post
    template_name = 'news/default.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(post_type='news').order_by('-created_at')

# Поиск новостей на основе django-filter и пагинации
class NewsSearchView(FilterView):
    model = Post
    filterset_class = PostFilter
    template_name = 'news/news_search.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(post_type='news').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # В контекст добавляем request для пагинации с параметрами
        context['request'] = self.request
        return context

# Создание новости
class NewsCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.post_type = 'news'
        form.instance.created_at = timezone.now()
        return super().form_valid(form)

# Редактирование новости
class NewsUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='news')

# Удаление новости
class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='news')

# Детальный просмотр новости
class NewsDetailView(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'item'

    def get_queryset(self):
        return Post.objects.filter(post_type='news')

# Список статей с пагинацией
class ArticlesListView(ListView):
    model = Post
    template_name = 'articles/articles_list.html'
    context_object_name = 'articles_list'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(post_type='article').order_by('-created_at')

# Создание статьи
class ArticleCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('articles_list')

    def form_valid(self, form):
        form.instance.post_type = 'article'
        form.instance.created_at = timezone.now()
        return super().form_valid(form)

# Редактирование статьи
class ArticleUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('articles_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='article')

# Удаление статьи
class ArticleDeleteView(DeleteView):
    model = Post
    template_name = 'articles/article_confirm_delete.html'
    success_url = reverse_lazy('articles_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='article')