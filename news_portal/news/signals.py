from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.db.models import Q

from django.core.mail import EmailMultiAlternatives

from news.models import *

@receiver(m2m_changed)
def subscription_event(instance: Post, **kwargs):
    if kwargs['action'] == 'post_add' and type(instance) == Post:
        # categories = instance.category.all()

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