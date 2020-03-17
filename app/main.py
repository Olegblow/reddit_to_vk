from __future__ import absolute_import
from __future__ import unicode_literals

import os

from celery import Celery
from celery.schedules import crontab
from download import start_download
from upload import start_upload


# RabbitMQ broker settings
# -----------------------------------------------------------------------------

RABBIT_HOST = os.getenv('RABBITMQ_DEFAULT_VHOST', '')
RABBIT_PORT = '5672'
BROKER_USER = os.getenv('RABBITMQ_DEFAULT_USER', '')
BROKER_PASSWORD = os.getenv('RABBITMQ_DEFAULT_PASS', '')
HOST = os.getenv('RABBIT_HOST', '@localhost:')
CELERY_BROKER_URL = ('amqp://' + BROKER_USER + ':' + BROKER_PASSWORD + HOST + RABBIT_PORT + '/' + RABBIT_HOST)
CELERY_RESULT_BACKEND = ('rpc://' + BROKER_USER + ':' + BROKER_PASSWORD + HOST + RABBIT_PORT + '/' + RABBIT_HOST)
EVERY_DAY_DOWNLOAD = crontab(minute=0, hour=0, day_of_month='*/1')
EVERY_DAY_UPLOAD = crontab(minute=0, hour=1, day_of_month='*/1')

# celery app
# ------------------------------------------------

app = Celery(
    'tasks',
    backend=CELERY_RESULT_BACKEND,
    broker=CELERY_BROKER_URL
)
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
)
app.conf.beat_schedule = {
    'download-every-40': {
        'task': 'main.download_task',
        'schedule': EVERY_DAY_DOWNLOAD,
    },
    'upload-every-day': {
        'task': 'main.upload_task',
        'schedule': EVERY_DAY_UPLOAD,
    },
}

if __name__ == '__main__':
    app.start()

# tasks
# ----------------------------------------------------


@app.task
def debug_task():
    """Дебаг таск."""
    print('debug')
    return 'return debug'


@app.task
def download_task() -> None:
    """Переодическая задача для загрузки файлов на сервер."""
    start_download()


@app.task
def upload_task() -> None:
    """Переодическая задача для загрузки файлов в вк."""
    start_upload()
