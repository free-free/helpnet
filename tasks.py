# coding=utf-8

import time
import json
from datetime import datetime

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
            req_param['url'] = "http://www.huzhugc.com/user/postedhelp/"
            req_param['data'] = {}
            req_param['data']['first']={"value":"你好，有人接受了你的求助","color":"#000"}
            req_param['data']['keyword1'] = {"value":do_username, "color":"#173177"}
            req_param['data']['keyword2'] = {"value":post_username, "color":"#173177"}
            req_param['data']['keyword3'] = {"value":p_datetime, "color":"#173177"}
            req_param['data']['remark'] = {"value":"Ta的联系方式 : "+do_usercontact,"color":"#173177"}
            redis = Redis("localhost", 6379)
            access_token = redis.get("weixin_api_token")
            access_token = access_token.decode()
            req_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={0}"
            req_url = req_url.format(access_token)
            req = requests.post(req_url , data=json.dumps(req_param))
            resp = req.json()
            if resp['errmsg'] != "ok":
                send_help_solved_msg(uid,
                                    do_username,
                                    do_usercontact,
                                    do_usercontact_means,
                                    post_username,
                                    posttime,
                                    failed_cnt+1
                                    )
        except Exception as e:
            send_help_solved_msg(uid,
                                 do_username,
                                 do_usercontact,
                                 do_usercontact_means,
                                 post_username,
                                 posttime,
                                 failed_cnt+1
                                 )
    else:
        pass

@tasker.task
def update_help_expire(failed_cnt = 0):
    if failed_cnt < 3:
        now_tm = time.time()
        mongo = MongoClient("10.251.32.12", 4000)
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

if __name__ == '__main__':
    pass
    '''
    send_help_solved_msg("oCyhTwZIMGZr7Izq175-peLFZAF0",
                        "tornado",
                        "18281573692",
                        "1",
                        "leeon",
                        time.time()
                    )
    '''
    #update_help_expire()

