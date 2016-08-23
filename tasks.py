# coding=utf-8

from submail import submail

from tasker import tasker
from token_servo import token_refresh


@tasker.task
def wxapi_token_refresh():
    token_refresh()

@tasker.task
def send_mail():
    manager = submail.build("mail")
    mail = manager.mail()
    mail['to'] = '18281573692@163.com'
    mail['project'] = 'wIrmM3'
    mail['appid'] = 11635
    mail['signature'] = "7e3faf32a3ca595bc3e81ff121bcad38"
    mail.send("xsend")


