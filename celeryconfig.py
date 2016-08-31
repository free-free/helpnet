# coding=utf-8

from celery.schedules import crontab

CELERY_ACCEPT_CONTENT = ["json", "pickle"]
CELERY_TIMEZONE = "UTC"
CELERY_ENABLE_UTC = True
CELERYBEAT_SCHEDULE = {
    'access_token_refresh':{
        'task': 'tasks.wxapi_token_refresh',
        'schedule': crontab(minute='50', hour="*/1"),
        'args': ''
    },
    'jsapi_ticket_refresh':{
        'task': 'tasks.wxjsapi_ticket_refresh',
        'schedule': crontab(minute='55', hour="*/1"),
        'args':''
    },
}
