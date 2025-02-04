import os
from celery import Celery
from celery.schedules import crontab
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')
 
app = Celery('news_portal')
app.config_from_object('django.conf:settings', namespace = 'CELERY')
app.conf.beat_schedule = {
    'ts_sending_out_new_posts': {
        'task': 'news.tasks.ts_sending_out_new_posts',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        # 'schedule': crontab(hour=17, minute=35),
        'args': (),
    },
}
app.autodiscover_tasks(['news'])