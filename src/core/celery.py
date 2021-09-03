from celery import Celery


app = Celery('core')
app.config_from_object('core.celeryconfig')
app.autodiscover_tasks()

app.conf.timezone = "Asia/Almaty"
