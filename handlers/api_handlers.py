# coding:utf-8

from tornado import gen,web
from .base_handler import BaseHandler,AuthNeedBaseHandler
import json
from . import send_async_request


class WeixinQRCodeAPIHandler(BaseHandler):

    r"""
        @url:/resource/WXQRCodeResource/get/?
    """ 
    @gen.coroutine
    def get(self):
        qrcode_ticket = yield self.application.cache.sget('weixin_qrcode_ticket')
        if qrcode_ticket:
            url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket="+qrcode_ticket
            self.set_header("Cache-Control","no-cache")
            self.write({"qrcode_url":url})
        else:
            token = yield self.application.cache.sget("weixin_api_token")
            url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token="+token
            body = {"expire_seconds": 86400, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": 123}}}
            body = json.dumps(body)
            try:
                response = yield send_async_request(url, method="POST", body=body)
                response = response.body.decode("utf-8")
                response = json.loads(response)
                if "ticket" in response:
                    url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket="+response["ticket"]
                    yield self.application.cache.set("weixin_qrcode_ticket",response["ticket"])
                    yield self.application.cache.expire("weixin_qrcode_ticket",response.get("expire_seconds",0))
                    self.write({"qrcode_url":url})
                else:
                    self.set_header("Cache-Control","no-cache")
                    self.write({"errmsg":"can't get qrcode","errcode":40002})
            except Exception as e:
                print(e)
                self.write({"errmsg":"can't get qrcode","errcode":40001})
    


class HelpContentAPIHandler(AuthNeedBaseHandler):
   
    r"""
        @url:/resource/HelpContentResource/get/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        source_url = self.get_argument("source_url")
        data = self.get_argument("data",{})
        longitude = data.get("longitude")
        latitude = data.get("latitude")
        offset = data.get("offset")
        if not longitude or not latitude:
            longitude = self.current_user['longitude']
            latitude = self.current_user['latitude']
        try:
            cursor =  self.application.db['help'].find({  \
                "location":{"$geoWithin":{"$center":[[longitude,latitude],0.1]}} })
            cursor.sort("posttime",1).limit(10).skip(offset)
            helpdata=[]
            while (yield cursor.fetch_next):
                dataline = curosr.next_object()
                del dataline['_id']
                helpdata.append(dataline)
            response = {}
            response['data']={}
            response['data']['offset'] = offset+10
            response['data']['helpdata'] = helpdata
            self.write(response)
        except Exception:
            self.write({"errcode":40002,"errmsg":"no data"})
           
            
      
        
                
