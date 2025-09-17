from celery import Celery

celery_app = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/1'
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