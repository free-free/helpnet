#-*- coding:utf-8 -*-

from tornado import gen,web

#
# weixin callback url handler
class CallbackHandler(web.RequestHandler):
    
    @gen.coroutine
    def get(self):
        self.write("callback handler")
    
    @gen.coroutine
    def post(self):
        print(self.request.body)
