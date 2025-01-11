from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.db.models import Q

from django.core.mail import EmailMultiAlternatives

from news.models import *

@receiver(m2m_changed)
def subscription_event(instance: Post, **kwargs):
    if kwargs['action'] == 'post_add' and type(instance) == Post:
        categories = instance.category.all()
        list_of_users = set()
        for category in categories:
            # print()
            # print('category:', category)
            # print()
            users = Subscriber.objects.filter(category__id__in = category.id) #, user__email__)
            for user in users:
                list_of_users.add(user)
        list_of_users = list(list_of_users)   
        print()
        print('kwargs[\'action\']', kwargs['action'])
        print()
        print('list_of_users', list_of_users)
        print()
    # if kwargs['action'] == 'post_add':
        # print()
        # print('sender', sender)
        # print()
        # print('instance', instance)
        # print()