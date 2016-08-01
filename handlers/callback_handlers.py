#-*- coding:utf-8 -*-

from tornado import gen,web
from base_handlers import BaseHandler

#
# weixin callback url handler
class CallbackHandler(web.RequestHandler):
    
    @gen.coroutine
    def get(self):
        pass
    
    @gen.coroutine
    def post(self):
        pass
