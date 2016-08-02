#-*- coding:utf-8 -*-

from tornado import gen,web
import xml.etree.ElementTree as etree
#
# weixin callback url handler
class CallbackHandler(web.RequestHandler):
    
    @gen.coroutine
    def get(self):
        self.write("callback handler")
    
    @gen.coroutine
    def post(self):
        root = etree.fromstring(self.request.body)
        print(root.findtext("ToUserName"))
      
