'''
Daily celery task to synchronize currencies
with an online service.
'''
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_task.settings')

app = Celery('test_task')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'download_currency': {
        'task': 'wallet.tasks.daily_request',
        'schedule': crontab(),
    },
}