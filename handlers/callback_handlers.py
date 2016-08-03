#-*- coding:utf-8 -*-

from tornado import gen,web
import xml.etree.ElementTree as etree
from .base_handler import BaseHandler
#
# weixin callback url handler
class CallbackHandler(BaseHandler):
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
        r"""
        request  link msg keys:
            Title
            Description
            Url
        """
        self.write(self.get_request_msg("MsgType"))

    def handle_event(self):
        r"""
        request evet msg keys:
           Event = subscribe/unsubscribe:
               EventKey:qrscene_*
               Ticket: 
           Event = SCAN:
               EventKey:int32(scene_id)
               Ticket:
           Event = LOCATION:
               Latitude:
               Longitude:
               Precision:
           Event = CLICK:
               EventKey:
           Event = VIEW:
               EventKey: url
           Event = TEMPLATESENDJOBFINISH
               Status:
        """
        event_type = self.get_request_msg("Event").lower()
        getattr(self,'handle_'+event_type+'_event',self.handle_other)()
  
    def handle_location_event(self):
        user_openid = self.get_request_msg("FromUserName")
        latitude = self.get_request_msg("Latitude")
        longitude = self.get_request_msg("Longitude")
        create_time = self.get_request_msg("CreateTime")
        self.write(latitude) 
    def handle_other(self):
        self.write("")

    @gen.coroutine
    def post(self):
        msg_type = self.get_request_msg("MsgType")
        getattr(self,'handle_'+msg_type,self.handle_other)()
        
      
