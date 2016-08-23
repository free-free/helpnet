# coding:utf-8

from tornado import gen,web
from .base_handler import BaseHandler,AuthNeedBaseHandler
import json
from . import send_async_request


class WeixinQRCodeGetAPIHandler(BaseHandler):

    r"""
        @url:/resource/WXQRCodeResource/get/?
    """ 
    @gen.coroutine
    def get(self):
        source_url = self.get_argument("source_url")
        data = self.get_argument("data")
        data = data or {}
        context = data.get("context")
        qrc = data.get("qrc")
        try:
            qrcode_ticket = yield self.application.cache.sget('weixin_qrcode_ticket')
            if qrcode_ticket:
                url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket="+qrcode_ticket
                response = {}
                response['qrc'] = qrc
                response['data'] = []
                response['data'].append({"qrcode_url": url})
                self.write(response)
            else:
                token = yield self.application.cache.sget("weixin_api_token")
                url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token="+token
                body = {"expire_seconds": 86400, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": 123}}}
                body = json.dumps(body)
                response = yield send_async_request(url, method="POST", body=body)
                response = response.body.decode("utf-8")
                response = json.loads(response)
                if "ticket" in response:
                    url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket="+response["ticket"]
                    yield self.application.cache.set("weixin_qrcode_ticket",response["ticket"])
                    yield self.application.cache.expire("weixin_qrcode_ticket",response.get("expire_seconds",0))
                    response = {}
                    response['qrc'] = qrc
                    response['data'] = []
                    response['data'].append({'qrcode_url':url})
                    self.write(response)
                else:
                    self.write({"errmsg":"can't get qrcode","errcode":40001})
        except Exception:  
            self.write({"errmsg":"can't get qrcode","errcode":40001})


class HelpContentGetAPIHandler(AuthNeedBaseHandler):
  
    valid_req_urls=[
        "/",
        "/user/posthelp/",
        "/user/gethelp/",
    ]
    r"""
        @url:/resource/HelpContentResource/get/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        source_url = self.get_argument("source_url")
        if source_url not in self.valid_req_urls:
            err_res = {}
            err_res["errcode"] = 40000
            err_res["errmsg"] = "not correct source_url"
            self.write(err_res)
        data = self.get_argument("data") or {}
        context = data.get("context")  
        qrc = data.get("qrc")
        yield getattr(context+'help',self.default)(qrc)
   
    @gen.coroutine
    def updateshelp(self,qrc): 
        longitude = qrc.get("lng")
        latitude = qrc.get("lat")
        last_help_pt = qrc.get("last_help_pt")
        if not longitude or not latitude:
            longitude = self.current_user['longitude']
            latitude = self.current_user['latitude']
        try:
            if last_help_pt <= 0:
                query = {"location":{"$geoWithin":{"$center":[[longitude,latitude],0.1]}}}
            else:
                query = {"location":{"$geoWithin":{"$center":[[longitude,latitude],0.1]}},"posttime":{"$lt":last_help_pt}}
            cursor = self.application.db['help'].find(query)
            cursor.sort("posttime",1).limit(10)
            helpdata=[]
            while (yield cursor.fetch_next):
                dataline = curosr.next_object()
                del dataline['_id']
                helpdata.append(dataline)
            qrc["last_help_pt"] = helpdata[-1].get("posttime",0)
            response = {}
            response['res_qrc'] = qrc
            response['data'] = helpdata
            self.write(response)
        except Exception:
            self.write({"errcode":50000,"errmsg":"server internal error"})

    @gen.coroutine
    def uposthelp(self,qrc):
        last_help_pt = qrc.get("last_help_pt")
        try:
            userid = self.current_user["userid"]
            if last_help_pt <= 0:
                query = {"post_userid":userid}
            else:
                query = {"post_userid":userid,"posttime":{"$lt":last_help_pt}}
            cursor = self.application.db['help'].find(query)
            cursor.sort("posttime",1).limit(10)
            helpdata = []
            while (yield cursor.fetch_next):
                dataline = cursor.next_object()
                del dataline['_id']
                helpdata.append(dataline)
            qrc["last_help_pt"] = helpdata[-1].get('posttime',0)
            response  = {}
            response['res_qrc'] = qrc
            response['data'] = posthelpdata
            self.write(response)
        except Exception:
            self.write({"errcode":50000,"errmsg":"server internal error"})
    
    @gen.coroutine
    def ugethelp(self,qrc):
        last_help_pt = qrc.get("last_help_pt")
        try:
            userid = self.current_user['userid'] 
            if last_help_pt <= 0:
                query = {"get_userid":userid}
            else:
                query = {"get_userid":userid,"posttime":{"$lt":last_help_pt}}
            cursor = self.application.db['help'].find(query)
            cusor.sort("posttime",1).limit(10)
            helpdata = []
            while (yield cursor.fetch_next):
                dataline = cursor.next_object()
                del dataline['_id'] 
                helpdata.append(dataline)
            qrc['last_help_pt'] = helpdata[-1].get("posttime",0)
            response = {}
            response['res_qrc'] = qrc
            response['data'] = helpdata
            self.write(response)
        except Exception:
            self.write({"errcode":50000,"errmsg": "server internal error"})

    @gen.coroutine
    def default(self,qrc):
        response = {}
        response['res_qrc'] = qrc
        response['data'] = []
        self.write(response)



class UserProfileGetAPIHandler(AuthNeedBaseHandler):
   
    r"""
        @url:/resource/UserProfileResource/get/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        source_url = self.get_argument("source_url","")
        if source_url != "/user/profile/":
            err_res = {}
            err_res["errcode"] = 40000
            err_res["errmsg"] = "not correct source_url"
            self.write(err_res)
        data = self.get_argument("data") or {}
        qrc = data.get("qrc")
        context = data.get("context")
        res = {}
        res["res_qrc"] = qrc
        res["data"] = []
        profile = {}
        profile['user_contact'] = self.current_user['usercontact']
        res["data"].append(profile)
        self.write(res)


class UserProfileUpdateAPIHandler(AuthNeedBaseHandler):

    r"""
        @url:/resource/UserProfileResource/update/?
    """
    @web.authenticated
    @gen.coroutine
    def post(self):
        source_url = self.get_argument("source_url","")
        if source_url != "/user/profile/":
            err_res = {}
            err_res["errcode"] = 40000
            err_res["errmsg"] = "not correct source_url"
            self.write(err_res)
        data = self.get_argument("data") or {}
        context = data.get("context",{})
        updates_profile = {}
        updates_profile['usercontact'] = context.get("user_contact","")
        qrc = data.get("qrc",{})
        try:
            self.session["usercontact"] = updates_profile["usercontact"]
            userid = self.current_user['userid']
            yield self.application.db['user'].update({"userid":userid},{"$set":updates_profile})
        except Exception:
            err_res={}
            err_res["errcode"] = 50000
            err_res["errmsg"] = "server internal error"
            self.write(err_res)
        res = {}
        res["res_qrc"] = qrc
        res["data"] = []
        self.write(res)
        
      
        
                
