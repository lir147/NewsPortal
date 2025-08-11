from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
import django_filters
from django_filters.views import FilterView
from django import forms
from .models import Post, Comment, Article, Subscription, Category
from .forms import CommentForm, RegisterForm, SubscriptionForm, PostForm
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import pytz
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect('news_list')


def toggle_theme(request):
    if 'dark_mode' not in request.session:
        request.session['dark_mode'] = True
    else:
        request.session['dark_mode'] = not request.session['dark_mode']

    # Для AJAX-запросов возвращаем JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'dark_mode': request.session['dark_mode']})

    return redirect(request.META.get('HTTP_REFERER', '/'))


def set_timezone(request):
    if request.method == 'POST':
        tz = request.POST.get('timezone')
        if tz in pytz.all_timezones:
            request.session['django_timezone'] = tz
            if hasattr(request.user, 'userprofile'):
                request.user.userprofile.timezone = tz
                request.user.userprofile.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return HttpResponseBadRequest("Invalid timezone")


# Фильтрация постов
class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label=_('Название'))
    author__user__username = django_filters.CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label=_('Автор')
    )
    created_at = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label=_('После даты'),
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = Post
        fields = ['title', 'author__user__username', 'created_at']

# Отписка от категории
@login_required
def unsubscribe(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    Subscription.objects.filter(user=request.user, category=category).delete()
    return redirect('manage_subscriptions')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

# Управление подписками
@login_required
def manage_subscriptions(request):
    user = request.user
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            selected_categories = form.cleaned_data['categories']
            Subscription.objects.filter(user=user).delete()
            for cat in selected_categories:
                Subscription.objects.create(user=user, category=cat)
            return redirect('profile')
    else:
        initial_cats = [sub.category for sub in user.subscriptions.all()]
        form = SubscriptionForm(initial={'categories': initial_cats})
    return render(request, 'subscriptions/manage.html', {'form': form})

# Лайк/дизлайк для статей
@login_required
@require_POST
def article_like(request, pk):
    article = get_object_or_404(Post, pk=pk, post_type='article')
    article.like()
    return redirect('article_detail', pk=pk)

@login_required
@require_POST
def article_dislike(request, pk):
    article = get_object_or_404(Post, pk=pk, post_type='article')
    article.dislike()
    return redirect('article_detail', pk=pk)

# Лайк/дизлайк для новостей
@login_required
@require_POST
def news_like(request, pk):
    news = get_object_or_404(Post, pk=pk, post_type='news')
    news.like()
    return redirect('news_detail', pk=pk)

@login_required
@require_POST
def news_dislike(request, pk):
    news = get_object_or_404(Post, pk=pk, post_type='news')
    news.dislike()
    return redirect('news_detail', pk=pk)

# Стать автором
@login_required
@require_POST
def become_author(request):
    authors_group, _ = Group.objects.get_or_create(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        request.user.groups.add(authors_group)
        request.user.save()
    return redirect('profile')

# Просмотр новости с комментариями
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

# Главная новостная страница
@method_decorator(cache_page(60), name='dispatch')
class NewsListView(ListView):
    model = Post
    template_name = 'news/default.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(post_type='news').order_by('-created_at')

# Поиск новостей
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

# Список статей
class ArticlesListView(ListView):
    model = Post
    template_name = 'articles/articles_list.html'
    context_object_name = 'articles_list'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(post_type='article').order_by('-created_at')

# Создание новости
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

# Обновление новости
class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.change_post'

    def get_queryset(self):
        return Post.objects.filter(post_type='news')

# Удаление новости
class NewsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.delete_post'

    def get_queryset(self):
        return Post.objects.filter(post_type='news')

# Создание статьи
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

# Обновление статьи
class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('articles_list')
    permission_required = 'news.change_post'

    def get_queryset(self):
        return Post.objects.filter(post_type='article')

# Просмотр статьи с кэшированием
@method_decorator(cache_page(60 * 5), name='dispatch')
class ArticleDetailView(DetailView):
    model = Post
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return Post.objects.filter(post_type='article')

# Удаление статьи
class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'articles/article_confirm_delete.html'
    success_url = reverse_lazy('articles_list')
    permission_required = 'news.delete_post'

    def get_queryset(self):
        return Post.objects.filter(post_type='article')

# Регистрация пользователя
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

# Детальный просмотр поста
class PostDetail(DetailView):
    model = Post
    template_name = 'news/post_detail.html'

def csrf_failure(request, reason=""):
    context = {'reason': reason}
    return render(request, 'csrf_failure.html', context)