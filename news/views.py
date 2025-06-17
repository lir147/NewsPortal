from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class ArticleListView(ListView):
    model = Post
    template_name = 'news/article_list.html'
    context_object_name = 'articles'

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
