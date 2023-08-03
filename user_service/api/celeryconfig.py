from celery import Celery

app = Celery('api.celery_app')

app.conf.broker_url = 'pyamqp://guest@localhost//'

app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']

app.conf.imports = ('api.celery_app',)

app.conf.beat_schedule = {
    'send-article-count-notifications': {
        'task': 'api.celery_app.send_article_count_notifications',
        'schedule': 1,
    },
}

