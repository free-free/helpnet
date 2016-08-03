#-*- coding:utf-8 -*-

from tornado import gen,web
import xml.etree.ElementTree as etree
#
# weixin callback url handler
class CallbackHandler(web.RequestHandler):
    r'''
       Request Message common keys:
           ToUserName: receive user name
           FromUserName: sending user name
           CreateTime: timestamp
           MsgType: 
           MsgId: int64
    '''

    def get_request_msg(self,name,default=None):
        if not hasattr(self,"__msg"):
            self.__msg = etree.fromstring(self.request.body)
        msg_val = self.__msg.findtext(name) or default
        return msg_val

    def handle_text(self):
        r"""
        request text msg keys:
           Content
        """
        self.write(self.get_request_msg("MsgType"))

    def handle_image(self):
        r"""
         request image msg keys:
                PicUrl
        """            
        self.write(self.get_request_msg("MsgType"))

    def handle_event(self):
        self.write(self.get_request_msg("MsgType"))
   
    def handle_location(self):
        r"""
        request location msg keys:
            Location_X
            Location_Y
            Scale
            Label
        """    
        self.write(self.get_request_msg("MsgType"))

    def handle_link(self):
        self.write(self.get_request_msg("MsgType"))

    def handle_other(self):
        self.write("")

    @gen.coroutine
    def get(self):
        self.write("callback handler")
    
    @gen.coroutine
    def post(self):
        msg_type = self.get_request_msg("MsgType")
        getattr(self,'handle_'+msg_type,'handle_other')()
        
      
