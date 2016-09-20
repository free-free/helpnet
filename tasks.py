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
def send_help_sovled_msg(uid, d_name, d_uct, d_uctm, content):
    if ductm == "1":
        d_uct += "(电话)"
    elif d_uctm == "2":
        d_uct += "(微信)"
    else:
        d_uct += "(QQ)"
    req_param = {}
    req_param['userid'] = userid
    req_param['template_id'] = ""
    req_param['url'] = "http://www.huzhugc.com/user/postedhelp/"
    req_param['data'] = {}
    req_param['data']['first']={"value":"","color":"#173177"}
    req_param['data']['do_username'] = {"value":d_name, "color":"#173177"}
    req_param['data']['do_usercontact'] = {"value":d_uct, "color":"#173177"}
    req_param['data']['content'] = {"value":content, "color":"#173177"}
    req_param['data']['remark'] = ""
    redis = Redis("localhost", 6379)
    access_token = redis.get("weixin_api_token")
    access_token = access_token.decode()
    req_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={0}"
    req_url = req_url.format(access_token)
    req = requests.post(req_url , data=req_param)
    resp = req.json()

@tasker.task
def update_help_expire():
    now_tm = time.time()
    mongo = MongoClient("localhost", 4000)
    temp_help = mongo['hnet']['permanent_help']
    updates_help = mongo['hnet']['updates_help']
    criteria = {"expiretime":{"$lt":now_tm}}
    modifier = {"$set":{"state":2}}
    try:
        resp1 = updates_help.remove(criteria, modifier)
        resp2 = temp_help.update(criteria, modifier)
    except Exception as e:
        update_help_expire()
   
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

