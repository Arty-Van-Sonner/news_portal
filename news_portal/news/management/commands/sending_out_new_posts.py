import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives as MSG

from datetime import datetime
from django.utils import timezone
from django.db.models import Q

from news.models import *
from pytz import timezone
from mailing.sending_mail import send_mail

logger = logging.getLogger(__name__)

def get_mytimezone_date(original_datetime, **kwargs):
    # new_datetime = datetime.strptime(original_datetime, '%Y-%m-%d')
    tz = timezone.get_current_timezone()
    timzone_datetime = timezone.make_aware(original_datetime, tz, True)
    return timzone_datetime.date()

def sending_out_new_posts(*args, **kwargs):
    sending_out_new_posts_mailing = Mailing.get_sending_out_new_posts_mailing()
    begin_date = MailingLog.objects.filter(mailing = sending_out_new_posts_mailing).values_list('datetime', flat = True).order_by('-datetime').first()
    if begin_date is None:
        begin_date = datetime(year = 2000, month = 1, day = 1, tzinfo = timezone(settings.TIME_ZONE))
    posts = Post.objects.filter(creation_date__gt = begin_date, category__isnull = False).distinct()
    categories = posts.values_list('category', flat = True).distinct()
    list_names_of_categories = []
    for category in categories:
        log_dict = {}
        if type(category) == int:
            log_dict['str_category'] = str(Category.objects.get(id = category)) 
        else:
            log_dict['str_category'] = str(category)
        emails = User.objects.filter(
            Q(subscriber__category = category) & ~Q(email = '') & Q(email__isnull = False)
            ).values_list('email', flat=True).distinct()
        posts_by_category = Post.objects.filter(creation_date__gt = begin_date, category = category)
        log_dict['str_posts'] = [str(Post.objects.get(id = post_log)) if type(post_log) == int else str(post_log) for post_log in posts_by_category]
        list_names_of_categories.append(log_dict)
        if len(emails) == 0:
            continue
        obj_category = Category.objects.get(id = category)
        template = 'news/new_posts.html'
        subject = f'New posts in category {obj_category} after {begin_date}'

        text_content = ''
        for post in posts_by_category:
            post_type = 'news' if post.type == 'N' else 'article'
            text_content += f'Title: {post.title}\n' \
                + f'Preview: {post.preview()}\n\n' \
                + f'Link to the {post_type}: http://127.0.0.1:8000{post.get_absolute_url()}\n' \
                + '''----------------------------------------------
            
                '''
        
        context = {
            'category': obj_category,
            'posts': posts_by_category,
        }
        send_mail(emails, subject, template, context, text_content)

    posts_by_category_description = ''
    for log_dict in list_names_of_categories:
        posts_by_category_description += f'\n\n##{log_dict["str_category"]}:\n•	' + '\n•	'.join(log_dict["str_posts"]) 
    description = f'#[{datetime.now()}] Sending out new posts\n##Categories:\n•	' + "\n•	".join([category["str_category"] for category in list_names_of_categories]) + '\n' + posts_by_category_description
    mailing_log = MailingLog.objects.create(mailing = sending_out_new_posts_mailing, description = description)
    for post in posts:
        mailing_log.posts.add(post)
    

class Command(BaseCommand):
    help = "Runs sending out new posts."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone = settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            sending_out_new_posts,
            # trigger=CronTrigger(second = "*/10"),
            # trigger=CronTrigger(minute = "*/1"),
            trigger=CronTrigger(hour = '18', minute = '00', day_of_week = '4'),
            id="sending_out_new_posts",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'sending_out_new_posts'.")

        try:
            logger.info("Starting scheduler 'sending_out_new_posts'")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler 'sending_out_new_posts'")
            scheduler.shutdown()
            logger.info("Scheduler 'sending_out_new_posts' shut down successfully!")