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
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Comment
from .forms import CommentForm

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

@login_required
@require_POST
def news_like(request, pk):
    news = get_object_or_404(Post, pk=pk, post_type='news')
    news.rating += 1
    news.save()
    return redirect('news_detail', pk=pk)


@login_required
@require_POST
def news_dislike(request, pk):
    news = get_object_or_404(Post, pk=pk, post_type='news')
    news.rating -= 1
    news.save()
    return redirect('news_detail', pk=pk)


class NewsDetailViewWithComments(View):
    def get(self, request, pk):
        news = get_object_or_404(Post, pk=pk, post_type='news')
        form = CommentForm()
        comments = news.comments.all().order_by('-created_at')
        return render(request, 'news/news_detail.html', {'item': news, 'form': form, 'comments': comments})

    def post(self, request, pk):
        news = get_object_or_404(Post, pk=pk, post_type='news')
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.post = news
            comment.user = request.user
            comment.save()
            return redirect('news_detail', pk=pk)
        comments = news.comments.all().order_by('-created_at')
        return render(request, 'news/news_detail.html', {'item': news, 'form': form, 'comments': comments})


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['post_type', 'created_at']


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Название')
    author__user__username = django_filters.CharFilter(field_name='author__user__username', lookup_expr='icontains', label='Автор')
    created_at = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='После даты',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['title', 'author__user__username', 'created_at']


class NewsListView(ListView):
    model = Post
    template_name = 'news/default.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(post_type='news').order_by('-created_at')


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
        context['request'] = self.request  # Для корректной пагинации с параметрами
        return context


class NewsCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.post_type = 'news'
        form.instance.created_at = timezone.now()
        return super().form_valid(form)


class NewsUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='news')


class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='news')


class ArticlesListView(ListView):
    model = Post
    template_name = 'articles/articles_list.html'
    context_object_name = 'articles_list'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(post_type='article').order_by('-created_at')


class ArticleCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('articles_list')

    def form_valid(self, form):
        form.instance.post_type = 'article'
        form.instance.created_at = timezone.now()
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('articles_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='article')

class ArticleDetailView(DetailView):
    model = Post
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return Post.objects.filter(post_type='article')


class ArticleDeleteView(DeleteView):
    model = Post
    template_name = 'articles/article_confirm_delete.html'
    success_url = reverse_lazy('articles_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='article')