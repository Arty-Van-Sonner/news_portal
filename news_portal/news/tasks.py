from celery import shared_task
# import time

from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
# from django.dispatch import receiver
from news.management.commands.sending_out_new_posts import sending_out_new_posts
# from news_portal.celery import app

from .models import *


@shared_task
def ts_subscription_event(instance, **kwargs):
    if kwargs['action'] == 'post_add' and type(instance) == int:
        # categories = instance.category.all()
        instance = Post.objects.get(id = instance)
        emails = User.objects.filter(
            Q(subscriber__category__in = instance.category.all().values_list('id')) & ~Q(email = '') & Q(email__isnull = False)
            ).values_list('email', flat=True)
       
        post_type = 'news' if instance.type == 'N' else 'article'
        subject = f'New {post_type} in category {instance.category}'
        text_content = (
        f'Title: {instance.title}\n'
        f'Preview: {instance.preview()}\n\n'
        f'Link to the {post_type}: http://127.0.0.1:8000{instance.get_absolute_url()}'
        ) 

        html_content = (
            f'Title: {instance.title}<br>'
            f'Preview: {instance.preview()}<br><br>'
            f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
            f'Link to the {post_type}'
        )
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

@shared_task
def ts_sending_out_new_posts():
    print('Задача ts_sending_out_new_posts Запускается')
    sending_out_new_posts(mailing = Mailing.get_sending_out_new_posts_mailing_celery())
