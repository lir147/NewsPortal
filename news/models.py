from django.urls import reverse
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
import pytz

TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.all_timezones]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(
        max_length=50,
        choices=[(tz, tz) for tz in pytz.all_timezones],
        default='Europe/Moscow'
    )

    def __str__(self):
        return f"{self.user.username} ({self.timezone})"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        post_rating = sum(post.rating * 3 for post in self.post_set.all())

        # Используем правильное имя related_name для комментариев пользователя
        comments_rating = sum(comment.rating for comment in self.user.comment_set.all())

        # Используем правильное имя related_name для комментариев к постам автора
        comments_to_posts_rating = sum(
            comment.rating for post in self.post_set.all()
            for comment in post.comments.all()
        )

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

    def __str__(self):
        return f"{self.user.username} - {self.category.name}"


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
    is_published = models.BooleanField(default=True)

    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='post_dislikes', blank=True)

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def dislikes_count(self):
        return self.dislikes.count()

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
        if self.post_type == 'news':
            return reverse('news_detail', args=[str(self.pk)])
        elif self.post_type == 'article':
            return reverse('article_detail', args=[str(self.pk)])
        else:
            return '#'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'category')

    def __str__(self):
        return f"{self.post.title} - {self.category.name}"


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def dislikes_count(self):
        return self.dislikes.count()

    def __str__(self):
        return (self.content[:50] + '...') if len(self.content) > 50 else self.content

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()