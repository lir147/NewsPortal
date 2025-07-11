from django.contrib.auth.models import Group, User
from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from news.models import Post, Subscription, Category, PostCategory
from news.tasks import send_new_post_email

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        subscribers_emails = Subscription.objects.filter(
            category__in=instance.categories.all()
        ).values_list('user__email', flat=True).distinct()
        subscribers_emails = [email for email in subscribers_emails if email]
        if subscribers_emails:
            subject = f'Новая новость: {instance.title}'
            message = instance.content
            send_new_post_email.delay(subject, message, subscribers_emails)  # Отправка асинхронно через Celery

@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers_new_article(sender, instance, action, **kwargs):
    if action == 'post_add':
        categories = instance.categories.all()
        for category in categories:
            subs = Subscription.objects.filter(category=category).select_related('user')
            for sub in subs:
                user = sub.user
                if not user.email:
                    continue
                article_url = settings.SITE_URL + reverse('article_detail', args=[instance.pk])
                subject = f"Новая статья в категории {category.name}"
                html_message = render_to_string('emails/new_article.html', {
                    'user': user,
                    'article': instance,
                    'article_url': article_url,
                })
                plain_message = (
                    f"Здравствуйте, {user.username}!\n\n"
                    f"В категории {category.name} появилась новая статья: {instance.title}\n"
                    f"Прочитать: {article_url}"
                )
                try:
                    send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL,
                              [user.email], html_message=html_message, fail_silently=False)
                except Exception as e:
                    # Для продакшена лучше заменить print на логирование
                    print(f"Ошибка отправки письма {user.email}: {e}")

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.email:
        subject = "Добро пожаловать на News Portal!"
        message = f"Здравствуйте, {instance.username}!\n\nСпасибо за регистрацию на нашем новостном портале!"
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Ошибка отправки welcome-письма {instance.email}: {e}")

@receiver(user_signed_up)
def add_user_to_common_group(request, user, **kwargs):
    common_group, created = Group.objects.get_or_create(name='common')
    if not user.groups.filter(name='common').exists():
        user.groups.add(common_group)