# -*- coding:utf-8 -*-

import json
import os
import argparse
import logging
import sys
logging.basicConfig(level=logging.ERROR)
from urllib.parse import urlencode, unquote

import requests
from redis import Redis

from config import config

class JSAPITicketServo(object):
  
    def __init__(self, ticket_url):
        assert ticket_url
        self.__ticket_url = ticket_url
  
    def get_ticket(self):
        try:
            req = requests.get(self.__ticket_url)
            body = req.json()
            jsapi_ticket = body.get("ticket")
            return jsapi_ticket
        except Exception as e:
            logging.error(e)
            

class TokenServo(object):
     
    def __init__(self, appid, appsecret, token_url):
        assert appid
        assert appsecret
        assert token_url
        self.__appid = appid
        self.__appsecret = appsecret
        self.__token_url = token_url + "?grant_type=client_credential&appid={0}&secret={1}".format(self.__appid,self.__appsecret)
        self.__token = None
    
    def get_token(self):
        try:
            req =  requests.get(self.__token_url)
            body = req.json()
            self.__token = body.get("access_token")
            return self.__token 
        except Exception as e:
            logging.error(e)

        
def token_refresh():
    app_config = {}
    redis = Redis(config['redis']['host'], config['redis']['port'])
    servo = TokenServo(config.get('public_appid'),
                          config.get('public_secret'),
                          config.get("token_url")
                         )
    token = servo.get_token()
    redis.set("weixin_api_token",token)

def jsapi_ticket_refresh():
    jsapi_ticket_url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={0}&type=jsapi"
    redis = Redis(config['redis']['host'], config['redis']['port'])
    access_token = redis.get("weixin_api_token").decode()
    jsapi_ticket_url = jsapi_ticket_url.format(access_token)
    servo = JSAPITicketServo(jsapi_ticket_url)
    ticket = servo.get_ticket()
    redis.set("weixin_jsapi_ticket", ticket)
   
def create_weixin_menu():
    redis = Redis(config['redis']['host'], config['redis']['port'])
    access_token = redis.get("weixin_api_token")
    access_token = access_token.decode()
    url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token={0}"
    url = url.format(access_token)
    qs = {}
    qs['redirect'] = "http://www.huzhugc.com/feelback/"
    data = {"button":[
             {"type":"view","name":"开始互助","url":"http://www.huzhugc.com/wxpubloginredirect/"},
             {"type":"view","name":"反馈意见","url":"http://www.huzhugc.com/wxpubloginredirect/?"+urlencode(qs)}]}
    req = requests.post(url, json.dumps(data,ensure_ascii=False).encode("utf-8"))
    return req.json()


if __name__ == '__main__':
    operation_help = """
        operation can't be empty, must be equal to 'run'
    """
    target_help = """
        target can't be empty,
        target corresponding to following function
        0 : token_refresh(),jsapi_ticket_refresh(),create_weixin_menu()
        1 : create_weixin_menu()
        2 : token_refresh()
        3 : jsapi_ticket_refresh()
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", type=str, help=operation_help)
    parser.add_argument("target", type=tuple, help=target_help)
    args = parser.parse_args()
    if '0' in args.target:
        print('running all services')
        token_refresh()
        jsapi_ticket_refresh()
        print(create_weixin_menu())
    elif '1' in args.target:
        print('running create_weixin_menu()')
        print(create_weixin_menu())
    elif '2' in args.target:
        print('running token_refresh()')
        token_refresh()
    elif '3' in args.target:
        print('running jsapi_ticket_refresh()')
        jsapi_ticket_refresh()
    else:
        print("run nothing")
