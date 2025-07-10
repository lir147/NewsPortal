import logging
import apscheduler.jobstores.base

from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler import util
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.models import User
from news.models import Post, Category

logger = logging.getLogger(__name__)

@util.close_old_connections
def weekly_newsletter():
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

        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
                html_message=html_message,
            )
            logger.info(f"Sent weekly newsletter to {user.email}")
        except Exception as e:
            logger.error(f"Error sending newsletter to {user.email}: {e}")

def run():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    try:
        scheduler.remove_job(job_id="weekly_newsletter_job", jobstore="default")
    except apscheduler.jobstores.base.JobLookupError:
        pass

    scheduler.add_job(
        weekly_newsletter,
        trigger=IntervalTrigger(weeks=1),
        id="weekly_newsletter_job",
        max_instances=1,
        replace_existing=True,
        next_run_time=timezone.now()  # Запустить сразу при старте
    )

    scheduler.start()
    logger.info("Scheduler started!")