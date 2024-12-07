from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'search_project.settings')

app = Celery('search_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()