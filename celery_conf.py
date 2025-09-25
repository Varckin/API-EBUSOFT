from celery import Celery
from os import getenv

celery_app = Celery(
    'tasks',
    broker=getenv('REDIS_BROKER_URL'),
    backend=getenv('REDIS_RESULT_BACKEND')
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
)

celery_app.autodiscover_tasks(
    packages=['ytdlp'],
    related_name='celery_tasks',
    force=True
)

celery_app.autodiscover_tasks(
    packages=['base64_coder'],
    related_name='celery_tasks',
    force=True
)
