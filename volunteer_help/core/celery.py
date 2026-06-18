
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery(
    'core',
    broker='redis://127.0.0.1:6379/0',
    backend='redis://127.0.0.1:6379/0',
)


app.autodiscover_tasks()


# app = Celery('proj',broker='redis://localhost:6379/', backend='rpc://', include=['proj.tasks'])


