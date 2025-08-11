from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse  # импортируем reverse
from django.utils.translation import gettext as _
import pytz
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(
        max_length=50,
        choices=[(tz, tz) for tz in pytz.all_timezones],
        default='Europe/Moscow'
    )

    def __str__(self):
        return f"{self.user.username} ({self.timezone})"

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username  # username не переводится, так как это уникальный идентификатор

    def update_rating(self):
        post_rating = sum(post.rating * 3 for post in self.posts.all())
        comments_rating = sum(comment.rating for comment in Comment.objects.filter(user=self.user))
        comments_to_posts_rating = sum(comment.rating for post in self.posts.all() for comment in post.comments.all())
        self.rating = post_rating + comments_rating + comments_to_posts_rating
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subscriptions')

    class Meta:
        unique_together = ('user', 'category')

class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('article', _('Статья')),
        ('news', _('Новость')),
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title} ({self.get_post_type_display()})'

    def preview(self):
        return self.content[:124] + '...' if len(self.content) > 124 else self.content

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def get_absolute_url(self):
        """
        Возвращает URL детального просмотра, зависит от типа поста.
        Используйте в шаблонах и др. для удобного доступа.
        """
        if self.post_type == 'news':
            return reverse('news_detail', args=[str(self.pk)])
        elif self.post_type == 'article':
            return reverse('article_detail', args=[str(self.pk)])
        else:
            return '#'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return (self.text[:50] + '...') if len(self.text) > 50 else self.text

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class Article(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Возвращает URL детального просмотра статьи.
        """
        return reverse('article_detail', args=[str(self.pk)])