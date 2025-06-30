from django.shortcuts import render, redirect, get_object_or_404
from django_filters.views import FilterView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import django_filters
from django import forms
from .models import News, Post, Comment
from django.urls import reverse_lazy
from django.utils import timezone

class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Название')
    author__username = django_filters.CharFilter(field_name='author__username', lookup_expr='icontains', label='Имя автора')
    pub_date = django_filters.DateFilter(field_name='pub_date', lookup_expr='gte', label='Дата позже',
                                        widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = News
        fields = ['title', 'author__username', 'pub_date']


class NewsSearchView(FilterView):
    model = News
    template_name = 'news/news_search.html'
    context_object_name = 'filter'
    filterset_class = NewsFilter
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by('-pub_date')


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = ['pub_date']


class NewsCreateView(CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_form.html'
    success_url = '/news/'

    def form_valid(self, form):
        form.instance.pub_date = timezone.now()
        return super().form_valid(form)

class NewsUpdateView(UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_form.html'
    success_url = '/news/'

class NewsDeleteView(DeleteView):
    model = News
    template_name = 'news/news_confirm_delete.html'
    success_url = '/news/'

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            comment = Comment.objects.create(post=post, user=request.user, text=text)
            comment.save()
            messages.success(request, 'Комментарий добавлен успешно!')
        else:
            messages.error(request, 'Комментарий не может быть пустым.')
    return redirect('article_list')

def news_detail(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    context = {
        'item': news_item
    }
    return render(request, 'news/news_detail.html', context)

class ArticleListView(ListView):
    model = News  # или Post, зависит от структуры
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    ordering = ['-pub_date']

class NewsListView(ListView):
    model = News
    template_name = 'news/default.html'
    context_object_name = 'page_obj'
    paginate_by = 10
    ordering = ['-pub_date']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post  # или отдельно модель Статья, если есть
        exclude = ['post_type', 'pub_date']  # например, если есть

class ArticleCreateView(CreateView):
    model = Post  # или отдельная модель Article
    form_class = ArticleForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('articles_list')  # замените на нужный URL

    def form_valid(self, form):
        form.instance.post_type = 'article'  # если используете такое поле для разделения
        return super().form_valid(form)

class ArticleUpdateView(UpdateView):
    model = Post
    form_class = ArticleForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('articles_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='article')

class ArticleDeleteView(DeleteView):
    model = Post
    template_name = 'articles/article_confirm_delete.html'
    success_url = reverse_lazy('articles_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='article')