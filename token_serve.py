#coding:utf-8

import logging
logging.basicConfig(level=logging.ERROR)
from tornado.httpclient import AsyncHTTPClient
from tornado import web,gen
from tornado import ioloop
import json
from tornado_hbredis import  TornadoHBRedis
import os


class TokenServer(object):
     
    def __init__(self, appid, appsecret, token_url):
        assert appid
        assert appsecret
        assert token_url
        self.__appid = appid
        self.__appsecret = appsecret
        self.__token_url = token_url + "?grant_type=client_credential&appid={0}&secret={1}".format(self.__appid,self.__appsecret)
        self.__conn = AsyncHTTPClient()
        self.__token = None
    @gen.coroutine
    def get_token(self):
        try:
            response =  yield self.__conn.fetch(self.__token_url)
            body = response.body.decode("utf-8")
            if body:
                body = json.loads(body)
                self.__token = body.get("access_token")
                return self.__token 
        except web.HTTPError as e:
            logging.error(e)
        finally:
            self.__conn.close()
        
            

if __name__ == '__main__':    
    @gen.coroutine
    def token_refresh():
        app_config = {}
        redis = TornadoHBRedis('localhost',6379)
        with open(os.path.join(os.path.dirname(__file__),"service_account.json")) as f:
            app_config = json.load(f)
        server = TokenServer(app_config.get('app_id'),
                          app_config.get('app_secret'),
                          app_config.get("token_url")
                         )
        token = yield server.get_token()
        yield redis.set("weixin_api_token",token)
    loop = ioloop.IOLoop.current()
    loop.run_sync(token_refresh)
