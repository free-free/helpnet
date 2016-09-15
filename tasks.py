# coding=utf-8

import time
import json

import requests
from redis   import Redis
from submail import submail
from pymongo import MongoClient

from tasker import tasker
from services import token_refresh, jsapi_ticket_refresh


@tasker.task
def wxapi_token_refresh():
    token_refresh()

@tasker.task
def wxjsapi_ticket_refresh():
    jsapi_ticket_refresh()    

@tasker.task
def send_mail():
    manager = submail.build("mail")
    mail = manager.mail()
    mail['to'] = '18281573692@163.com'
    mail['project'] = 'wIrmM3'
    mail['appid'] = 11635
    mail['signature'] = "7e3faf32a3ca595bc3e81ff121bcad38"
    mail.send("xsend")

@tasker.task
def help_expire():
    now_tm = time.time()
    mongo = MongoClient("localhost", 4000)
    help_order = mongo['fsp']['help_order']
    criteria = {"expiretime":{"$lt":now_tm}}
    modifier = {"$set":{"state":2}}
    resp = help_order.update(criteria, modifier)
   
@tasker.task
def create_wx_menu():
    redis = Redis("localhost", 6379)
    access_token = redis.get("weixin_api_token")
    access_token = access_token.decode()
    url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token={0}"
    url = url.format(access_token)
    data = {
        "button":[
            {
	        "type": "view",
                "name": "寻求帮助",
                "url": "http://www.huzhugc.com/wxpubloginredirect/"
            },
	]
    }
    req = requests.post(url, data=data)
    return req.json()

