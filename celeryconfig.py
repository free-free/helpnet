# coding=utf-8

from celery.schedules import crontab

BROKER_URL = "redis://localhost:6379/1"
# CELERY_RESULT_BACKEND = "redis://"
CELERY_IMPORTS = ('worker', )

CELERY_ACCEPT_CONTENT = ["json", "pickle"]
CELERY_TASK_SERIALIZER = "json"

CELERY_TIMEZONE = "UTC"
CELERY_ENABLE_UTC = True
CELERYBEAT_SCHEDULE = {
    'access_token_refresh':{
        'task': 'worker.wxapi_token_refresh',
        'schedule': crontab(minute='50', hour="*/1"),
        'args': ''
    },
    'jsapi_ticket_refresh':{
        'task': 'worker.wxjsapi_ticket_refresh',
        'schedule': crontab(minute='55', hour="*/1"),
        'args':''
    },
    'update_help_expire':{
        'task': 'worker.update_help_expire',
        'schedule': crontab(minute='*/10'),
        'args':''
    }
}
