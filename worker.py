# coding=utf-8

import time
import json
from datetime import datetime
from urllib.parse import urlencode

import requests
from redis   import Redis
from submail import submail
from pymongo import MongoClient
from celery import Celery

from services import token_refresh, jsapi_ticket_refresh
from config import config

#tasker = Celery("tasker", broker="redis://localhost:6379/1", include=['tasks'])
tasker = Celery('worker')
tasker.config_from_object("celeryconfig")

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
def send_welcome_text(uid):
    redis = Redis(config['redis']['host'], config['redis']['port'])
    access_token = redis.get("weixin_api_token")
    access_token = access_token.decode()
    req_url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={0}"
    req_url = req_url.format(access_token)
    data = {}
    data['touser'] = uid
    data['msgtype'] = 'text'
    data['text'] = {}
    data['text']['content'] = "\n欢迎来到「互助广场」！\n\n「互助广场」\
是一个互相帮助的平台，在这里你可以发送求助，你周围的人来帮助你，并支付一定的小费给帮助你的人，\
同时你也可以帮助你周围的人。\n\n\
欢迎向我们反馈你对互助广场的改进意见，请点击底栏的\"反馈意见\"进入。\n\n\
请点击底栏\"开始互助\"进入互助广场。\n"
    req = requests.post(req_url, data=json.dumps(data,ensure_ascii=False).encode("utf-8"))
    return req.json()

@tasker.task
def send_failed_text(uid):
    redis = Redis(config['redis']['host'], config['redis']['port'])
    access_token = redis.get("weixin_api_token")
    access_token = access_token.decode()
    req_url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={0}"
    req_url = req_url.format(access_token)
    data = {}
    data['touser'] = uid
    data['msgtype'] = 'text'
    data['text'] = {}
    data['text']['content'] = "\n 关注公众号失败，请重新关注！\n"
    req = requests.post(req_url, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
    return req.json()

@tasker.task
def send_help_solved_msg(uid,
                         do_username, 
                         do_usercontact,
                         do_usercontact_means,
                         post_username, 
                         posttime,
                         failed_cnt=0):

    if failed_cnt < 3:
        try:
            if do_usercontact_means == "1":
                do_usercontact += "(电话)"
            elif do_usercontact_means == "2":
                do_usercontact += "(微信)"
            else:
                do_usercontact += "(QQ)"
            p_datetime = datetime.fromtimestamp(posttime)
            p_datetime = datetime.strftime(p_datetime, "%Y/%m/%d %H:%M")
            req_param = {}
            req_param['touser'] = uid
            req_param['template_id'] = "_lxGE1RWoMgEnj5eSQa96_eiuCo4PUMmjGMMRhZDlQU"
            qs_url = {}
            qs_url['redirect'] = "http://www.huzhugc.com/user/postedhelp/"
            qs_url['expiretime'] = 0
            req_param['url'] = "http://www.huzhugc.com/wxpubloginredirect/?"+urlencode(qs_url)
            req_param['data'] = {}
            req_param['data']['first']={"value":"你好，有人接受了你的求助","color":"#000"}
            req_param['data']['keyword1'] = {"value":do_username, "color":"#173177"}
            req_param['data']['keyword2'] = {"value":post_username, "color":"#173177"}
            req_param['data']['keyword3'] = {"value":p_datetime, "color":"#173177"}
            req_param['data']['remark'] = {"value":"Ta的联系方式 : "+do_usercontact,"color":"#173177"}
            redis = Redis(config['redis']['host'], config['redis']['port'])
            access_token = redis.get("weixin_api_token")
            access_token = access_token.decode()
            req_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={0}"
            req_url = req_url.format(access_token)
            req = requests.post(req_url , data=json.dumps(req_param))
            resp = req.json()
            if resp['errmsg'] != "ok":
                raise Exception("sending message failed")
        except Exception as e:
            send_help_solved_msg(uid,
                do_username,
                do_usercontact,
                do_usercontact_means,
                post_username,
                posttime,
                failed_cnt+1
            )

@tasker.task
def update_help_expire(failed_cnt = 0):
    if failed_cnt < 3:
        now_tm = time.time()
        mongo = MongoClient(config['mongodb']['host'], config['mongodb']['port'])
        permanent_help = mongo['hnet']['permanent_help']
        updates_help = mongo['hnet']['updates_help']
        modifier = {"$set":{"state":2}}
        try:
           criteria = {"$and":[{"expiretime":{"$lt":now_tm}},{"state":0}]}
           resp1 = permanent_help.update(criteria, modifier)
           criteria = {"expiretime":{"$lt": now_tm}}
           resp2 = updates_help.remove(criteria)
        except Exception as e:
           print(e)
           update_help_expire(failed_cnt+1)
    else:
        pass
 
if __name__ == '__main__':
    send_welcome_text("oCyhTwZIMGZr7Izq175-peLFZAF0")
