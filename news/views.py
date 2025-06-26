from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import News, Post, Comment

class ArticleListView(ListView):
    model = News  # или Post, в зависимости от задачи
    template_name = 'news/news_list.html'  # один шаблон
    context_object_name = 'news'  # имя переменной в шаблоне
    ordering = ['-pub_date']

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

def news_list(request):
    # Получаем все новости, отсортированные по убыванию даты публикации
    news = News.objects.order_by('-pub_date')
    context = {
        'news': news
    }
    return render(request, 'news/default.html', context)
