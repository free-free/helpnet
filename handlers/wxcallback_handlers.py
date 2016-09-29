#-*- coding:utf-8 -*-

import time
import json
import hashlib
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
        signature = self.get_argument("signature")
        nonce = self.get_argument("nonce")
        timestamp = self.get_argument("timestamp")
        token = self.application.settings['wx_callback_token']
        param_list = [token, timestamp, nonce]
        param_list.sort()
        param_str = ''.join(param_list).encode()
        sha1 = hashlib.sha1()
        sha1.update(param_str)
        param_str = sha1.hexdigest()
        if signature != param_str:
            self.write("")
            return 
        self.req_msg = xmltodict.parse(self.request.body)['xml']

    @gen.coroutine
    def handle_text(self):
        r"""
        request text msg keys:
           Content
        """
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
        try:
            user_openid = self.req_msg.get("FromUserName")
            user_existence = yield self.application.db['user'].find_one({"userid":user_openid},{"_id":1,"userid":1,"help_cnt":1})
            access_token = yield self.application.cache.sget('weixin_api_token') 
            url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token={0}&openid={1}&lang={2}"
            url = url.format(access_token,user_openid,"zh_CN")
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
            if user_existence:
                userdata['help_cnt'] = user_existence['help_cnt']
                userdata['_id'] = user_existence['_id']
            else:
                userdata['help_cnt'] = {"posted_help_num":0, "done_help_num":0}
            yield self.application.db['user'].save(userdata)
            self.application.task.send_task('worker.send_welcome_text', args=(user_openid,))
        except Exception as e:
            self.application.task.send_task("worker.send_failed_text", args=(user_openid,))
            self.write("failed")
            return 
        self.write("success")  

    @gen.coroutine
    def handle_unsubscribe_event(self):
        user_openid = self.req_msg.get("FromUserName")
        try:
            yield self.application.db['user'].update({"userid":user_openid},{"$set":{"subscribe":0}})
        except Exception as e:
            self.write("failed")
            return 
        self.write("success")
    
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
        
      
