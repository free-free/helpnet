# coding=utf-8

from celery.schedules import crontab

CELERY_ACCEPT_CONTENT = ["json", "pickle"]
CELERY_TIMEZONE = "UTC"
CELERY_ENABLE_UTC = True
CELERYBEAT_SCHEDULE = {
    'every-one-hour-and-fifty-minute':{
        'task': 'tasks.wxapi_token_refresh',
        'schedule': crontab(minute='*/50',hour="*/1"),
        'args': ''
    }
}
