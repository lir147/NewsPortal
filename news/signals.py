from django.contrib.auth.models import Group, User
from django.urls import reverse
from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from news.models import Post, Subscription


@receiver(post_save, sender=Post)
def notify_subscribers_new_article(sender, instance, created, **kwargs):
    if created and instance.post_type == 'article':
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
                    'category': category,
                })
                plain_message = f"Здравствуйте, {user.username}!\n\nВ категории {category.name} появилась новая статья: {instance.title}\nПрочитать: {article_url}"

                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    html_message=html_message,
                    fail_silently=False,
                )

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