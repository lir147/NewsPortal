from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
import django_filters
from django_filters.views import FilterView
from django import forms
from .models import Post, Comment, Article
from .forms import CommentForm, RegisterForm, ProfileForm
from django.contrib.auth import login


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


@login_required
@require_POST
def become_author(request):
    authors_group, _ = Group.objects.get_or_create(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        request.user.groups.add(authors_group)
        request.user.save()
    return redirect('profile')

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
        context['request'] = self.request
        return context


class ArticlesListView(ListView):
    model = Post
    template_name = 'articles/articles_list.html'
    context_object_name = 'articles_list'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(post_type='article').order_by('-created_at')


class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        form.instance.post_type = 'news'
        form.instance.created_at = timezone.now()
        return super().form_valid(form)


class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.change_post'

    def get_queryset(self):
        return Post.objects.filter(post_type='news')


class NewsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.delete_post'

    def get_queryset(self):
        return Post.objects.filter(post_type='news')


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('articles_list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        form.instance.post_type = 'article'
        form.instance.created_at = timezone.now()
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('articles_list')
    permission_required = 'news.change_post'

    def get_queryset(self):
        return Post.objects.filter(post_type='article')


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return Post.objects.filter(post_type='article')


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'articles/article_confirm_delete.html'
    success_url = reverse_lazy('articles_list')
    permission_required = 'news.delete_post'

    def get_queryset(self):
        return Post.objects.filter(post_type='article')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            common_group, created = Group.objects.get_or_create(name='common')
            user.groups.add(common_group)
            user.save()
            login(request, user)
            return redirect("news_list")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


