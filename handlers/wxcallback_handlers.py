#-*- coding:utf-8 -*-

import time
import json
from datetime import datetime

from tornado import gen,web
import xml.etree.ElementTree as etree
import xmltodict

from .base_handler import BaseHandler
from . import send_async_request
#
# weixin callback url handler

class WXCallbackHandler(BaseHandler):
    r'''
       Request Message common keys:
           ToUserName: receive user name
           FromUserName: sending user name
           CreateTime: timestamp
           MsgType: 
           MsgId: int64
    '''

    def prepare(self):
        super().prepare()
        self.req_msg = xmltodict.parse(self.request.body)['xml']

    @gen.coroutine
    def handle_text(self):
        r"""
        request text msg keys:
           Content
        """
        self.application.tasks.send_mail.delay()
        print("send mail")
        self.write("")
 
    @gen.coroutine
    def handle_image(self):
        r"""
         request image msg keys:
                PicUrl
        """            
        self.write("")

    @gen.coroutine
    def handle_location(self):
        r"""
        request location msg keys:
            Location_X
            Location_Y
            Scale
            Label
        """    
        self.write("")

    @gen.coroutine
    def handle_link(self):
        r"""
        request  link msg keys:
            Title
            Description
            Url
        """
        self.write("")

    @gen.coroutine
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
        event_type = self.req_msg.get("Event").lower()
        yield getattr(self,'handle_'+event_type+'_event',self.handle_other)()
  
    @gen.coroutine 
    def handle_location_event(self):
        user_openid = self.req_msg.get("FromUserName")
        user_exists = yield self.application.db.user.find_one({"userid":user_openid},{"userid":1})
        if user_exists:
            location = [float(self.req_msg.get("Longitude")), float(self.req_msg.get("Latitude"))]
            location_precision = self.req_msg.get("Precision")
            try:
                yield self.application.db.user.update({"userid":user_openid},\
                    {"$set":{"location":location,"locprec":location_precision}},\
                    upsert=True)
            except Exception:
                pass   
        self.write("success")

    @gen.coroutine
    def handle_subscribe_event(self):
        user_openid = self.req_msg.get("FromUserName")
        user_exists = yield self.application.db['user'].find_one({"userid":user_openid},{"userid":1})
        if not user_exists:
            try:
                access_token = yield self.application.cache.sget('weixin_api_token')
            except Exception as e:
                self.write("")
                return  
            if access_token:
                url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token={0}&openid={1}&lang={2}"
                url = url.format(access_token,user_openid,"zh_CN")
                try:
                    response = yield send_async_request(url)
                    userdata = json.loads(response.body.decode("utf-8"))
                    userdata['createtime'] = userdata.pop('subscribe_time',time.time()) 
                    userdata['userid'] = userdata.pop('openid')
                    userdata['username'] = userdata.pop('nickname')
                    userdata['address'] = ''
                    userdata['location'] = [0, 0]
                    del userdata['remark']
                    del userdata['groupid']
                    del userdata['tagid_list']
                    del userdata['language']
                    yield self.application.db['user'].insert(userdata)
                except Exception as e:
                    pass
                self.write("")  
        else: 
            self.write("") 

    @gen.coroutine
    def handle_unsubscribe_event(self):
        user_openid = self.req_msg.get("FromUserName")
        try:
            yield self.application.db.user.remove({"userid":user_openid})
        except Exception as e:
            pass
        self.write("")
    
    @gen.coroutine
    def handle_click_event(self):
        self.write("")
  
    @gen.coroutine
    def handle_view_event(self):
        self.write("") 

    @gen.coroutine
    def handle_other(self):
        self.write("")

    @gen.coroutine
    def post(self):
        msg_type = self.req_msg.get("MsgType")
        yield getattr(self,'handle_'+msg_type,self.handle_other)()
        
      
