from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.models import User
from news.models import Post, Subscription, Category

class Command(BaseCommand):
    help = "Еженедельная рассылка новых статей по подпискам"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        week_ago = now - timedelta(days=7)

        users = User.objects.filter(email__isnull=False)
        for user in users:
            categories = Category.objects.filter(subscriptions__user=user).distinct()
            articles = Post.objects.filter(
                categories__in=categories,
                created_at__gte=week_ago,
                post_type='article'
            ).distinct().order_by('-created_at')

            if not articles.exists():
                continue

            article_list = []
            for article in articles:
                url = settings.SITE_URL + reverse('article_detail', args=[article.pk])
                article_list.append({
                    'title': article.title,
                    'url': url,
                    'summary': article.content[:124] + ('...' if len(article.content) > 124 else ''),
                    'published': article.created_at,
                })

            subject = 'Еженедельная рассылка новых статей'
            html_message = render_to_string('emails/weekly_newsletter.html', {
                'user': user,
                'articles': article_list,
            })

            plain_message = f"Здравствуйте, {user.username}!\n\nНовые статьи за неделю:\n"
            for a in article_list:
                plain_message += f"- {a['title']}: {a['url']}\n"

            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=html_message,
            )