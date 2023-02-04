import logging
import os

from celery import Celery
from kombu import Queue

logger = logging.getLogger('celery.tasks')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.task_default_queue = 'default'
app.conf.task_queues = (
    Queue('default'),
)
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """Show tasks on worker load."""
    print('Request: {0!r}'.format(self.request))
