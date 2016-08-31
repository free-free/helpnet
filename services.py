#coding:utf-8

import json
import os
import logging
logging.basicConfig(level=logging.ERROR)

import requests
from redis import Redis

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
    redis = Redis('localhost',6379)
    with open(os.path.join(os.path.dirname(__file__),"service_account.json")) as f:
        app_config = json.load(f)
    servo = TokenServo(app_config.get('public_appid'),
                          app_config.get('public_secret'),
                          app_config.get("token_url")
                         )
    token = servo.get_token()
    redis.set("weixin_api_token",token)

def jsapi_ticket_refresh():
    jsapi_ticket_url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={0}&type=jsapi"
    redis = Redis("localhost", 6379)
    access_token = redis.get("weixin_api_token").decode()
    jsapi_ticket_url = jsapi_ticket_url.format(access_token)
    servo = JSAPITicketServo(jsapi_ticket_url)
    ticket = servo.get_ticket()
    redis.set("weixin_jsapi_ticket", ticket)
   
if __name__ == '__main__':
    token_refresh()
    jsapi_ticket_refresh()
