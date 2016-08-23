# coding=utf-8

from celery import Celery

tasker = Celery("tasker", broker="redis://localhost:6379/1", include=['tasks'])
tasker.config_from_object("celeryconfig")



