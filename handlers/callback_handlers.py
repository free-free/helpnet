#-*- coding:utf-8 -*-

from tornado import gen,web
import xml.etree.ElementTree as etree
#
# weixin callback url handler
class CallbackHandler(web.RequestHandler):
    r'''
       Request Message keys:
           ToUserName: receive user name
           FromUserName: sending user name
           CreateTime: timestamp
           MsgType: 
           Content:
           MsgId: int64
    '''

    def get_request_msg(self,name,default=None):
        if not hasattr(self,"__msg"):
            self.__msg = etree.fromstring(self.request.body)
        msg_val = self.__msg.findtext(name) or default
        return msg_val

    @gen.coroutine
    def get(self):
        self.write("callback handler")
    
    @gen.coroutine
    def post(self):
        msg_type = self.get_request_msg("MsgType")
        if msg_type == "text":
            pass
        
      
