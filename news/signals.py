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
def send_new_article_notification(sender, instance, created, **kwargs):
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
                html_content = render_to_string('emails/new_article.html', {
                    'user': user,
                    'article': instance,
                    'article_url': article_url,
                })
                plain_content = f"Здравствуйте, {user.username}!\nВ категории {category.name} вышла новая статья: {instance.title}\nЧитайте по ссылке: {article_url}"
                send_mail(subject, plain_content, settings.DEFAULT_FROM_EMAIL,
                          [user.email], html_message=html_content)



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