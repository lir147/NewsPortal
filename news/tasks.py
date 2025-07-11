from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
from .models import Post, Subscription

@shared_task
def weekly_newsletter():
    one_week_ago = now() - timedelta(days=7)
    recent_posts = Post.objects.filter(created_at__gte=one_week_ago)
    if not recent_posts.exists():
        return  # Нет свежих новостей за неделю

    subscribers_emails = Subscription.objects.all().values_list('user__email', flat=True).distinct()
    subscribers_emails = [email for email in subscribers_emails if email]

    subject = 'Еженедельная рассылка новостей'
    message_lines = [
        f"{post.title}\n{post.content}\n---" for post in recent_posts
    ]
    message = '\n\n'.join(message_lines)

    if subscribers_emails:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            subscribers_emails,
            fail_silently=False,
        )

@shared_task
def send_new_post_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )