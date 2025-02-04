from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.db.models import Q

from django.core.mail import EmailMultiAlternatives

from news.models import *

from .tasks import *

@receiver(m2m_changed)
def subscription_event(instance: Post, **kwargs):
    ts_subscription_event.delay(instance.id, **{'action': kwargs['action']})