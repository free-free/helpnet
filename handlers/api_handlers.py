# coding:utf-8

import json
import time
import hashlib
from datetime import datetime

from tornado import gen,web
import shortuuid

from .base_handler import BaseHandler,AuthNeedBaseHandler
from . import send_async_request


class APIBaseHandler(AuthNeedBaseHandler):
    
    @gen.coroutine
    def prepare(self):
        yield super().prepare()
        if self.request.headers.get("X-Requested-With") != "XMLHttpRequest":
            self.set_status(400)
            self.render("errors/400.html")
            return 
        self.source_url = self.get_argument("source_url")
        if hasattr(self, "_valid_urls"):
            if self.source_url not in self._valid_urls:
                self.write({"errcode":40000, "errmsg":"invalid source_url"})
                return 
        data = json.loads(self.get_argument("data")) or {}
        self.qrc = data.get("qrc") or {}
        self.context = data.get('context') or {}
        
        
class WeixinJSApiAPIHandler(APIBaseHandler):
    
    r"""
        @url:/resource/WXJSApiResource/get/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        try:
            jsapi_ticket = yield self.application.cache.sget("weixin_jsapi_ticket")
            if not jsapi_ticket:
                self.application.tasks.jsapi_ticket_refresh()
                jsapi_ticket = yield self.application.cache.sget("weixin_jsapi_ticket")
            appid = self.application.settings['public_appid']
            timestamp = str(int(time.time()))
            noncestr = shortuuid.uuid()
            url = self.context['req_url']
            unsort_params = {'url':url, 'timestamp':timestamp,
                'noncestr':noncestr, 'jsapi_ticket':jsapi_ticket}
            sort_params= [(k, unsort_params[k]) for k in sorted(unsort_params.keys())]
            params_str = '&'.join(map(lambda item: item[0]+'='+item[1], sort_params))
            sha1 = hashlib.sha1()
            sha1.update(params_str.encode())
            signature = sha1.hexdigest()
            response = {}
            response['resp_qrc'] = self.qrc
            response['resp'] = []
            response['resp'].append({'timestamp':timestamp,
                'appid':appid, 'noncestr':noncestr, 'signature':signature,
                'api_list':['openLocation','getLocation']
            })
            self.write(response)
        except Exception as e:
            self.write({"errmsg":"can't js api signature","errcode":40001})
               

class WeixinQRCodeGetAPIHandler(APIBaseHandler):

    r"""
        @url:/resource/WXQRCodeResource/get/?
    """ 
    @gen.coroutine
    def get(self):
        try:
            qrcode_ticket = yield self.application.cache.sget('weixin_qrcode_ticket')
            if qrcode_ticket:
                url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket="+qrcode_ticket
                response = {}
                response['resp_qrc'] = self.qrc
                response['resp'] = []
                response['resp'].append({"qrcode_url": url})
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
                    response['resp_qrc'] = self.qrc
                    response['resp'] = []
                    response['resp'].append({'qrcode_url':url})
                    self.write(response)
                else:
                    self.write({"errmsg":"can't get qrcode","errcode":40002})
        except Exception:  
            self.write({"errmsg":"can't get qrcode","errcode":40002})


class HelpResourceAPIHandler(APIBaseHandler):
    
    r"""
        @url:/resource/HelpResource/delete/?
    """
    @web.authenticated
    @gen.coroutine
    def delete(self):
        helpid = self.context.get("helpid",None)
        if not helpid:
            resp = {"errcode":40003,"errmsg":"invalid helpid"}
            self.write(resp);
            return 
        try:
            query = {"helpid":helpid,"post_userid":self.current_user['userid']}
            helpdata = yield self.application.db['temp_help'].find_one(query)
            resp = {}
            if helpdata:
                yield self.application.db['permanent_help'].remove(query)
                yield self.application.db['updates_help'].remove(query)
                criteria = {"userid":self.current_user['userid']}
                modifier = {"$inc":{"help_cnt.posted_help_num":-1}}
                yield self.application.db['user'].update(criteria, modifier)
                if helpdata['state'] == 1: 
                    criteria = {"userid":helpdata['do_userid']}
                    modifier = {"$inc":{"help_cnt.done_help_num":-1}}
                    yield self.application.db['user'].update(criteria, modifier)
                resp['resp'] = []
                resp['resp_qrc'] = {}
                resp['resp_qrc']['result'] = "OK"
                resp['resp_qrc']['code'] = 0
            else:
                resp['resp'] = []
                resp['resp_qrc'] = {}
                resp['resp_qrc']['result'] = "NO"
                resp['resp_qrc']['code'] = -1
            self.write(resp)
        except Exception  as e:
            print(e)
            self.write({"errcode":50000,"errmsg":"server internal error"})
       

class UpdatesHelpGetAPIHandler(APIBaseHandler):
  
    _valid_urls=[
        "/",
    ]
    r"""
        @url:/resource/UpdatesHelpResource/get/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        now_tm = time.time()
        last_help_pt = float(self.context.get("last_help_pt",0))
        location = self.context.get("location", self.current_user['location']);
        location[0] = float(location[0])
        location[1] = float(location[1])
        rcd_num = int(self.qrc.get("rcd_num", 0))
        rcd_cnt = 0
        try:
            if last_help_pt <= 0.0:
                query = {"location":{"$geoWithin":{"$center":[location,0.02]}},"state":0}
            else:
                query = {"location":{"$geoWithin":{"$center":[location,0.02]}},"state":0,"posttime":{"$lt":last_help_pt}}
            cursor = self.application.db['updates_help'].find(query)
            cursor.sort("posttime", -1).limit(rcd_num)
            helpdata=[]
            while (yield cursor.fetch_next):
                dataline = cursor.next_object()
                del dataline['_id']
                dataline['url'] = '/dohelp/'+dataline['helpid']+'/';
                dataline['post_datetime'] = datetime.isoformat(datetime.fromtimestamp(dataline['posttime']))
                if 'expiretime' in dataline and dataline['expiretime'] < now_tm:
                    continue 
                helpdata.append(dataline)
                rcd_cnt += 1
            if helpdata:
                self.qrc["last_help_pt"] = helpdata[-1].get("posttime",0)
            else:
                self.qrc["last_help_pt"] = last_help_pt
            self.qrc['rcd_num'] = rcd_cnt
            response = {}
            response['resp_qrc'] = self.qrc
            response['resp'] = helpdata
            self.write(response)
        except Exception as e:
            print(e)
            self.write({"errcode":50000,"errmsg":"server internal error"})


class PostedHelpGetAPIHandler(APIBaseHandler):

    r"""
        @url:/resource/PostedHelpResource/get/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        now_tm = time.time()
        last_help_pt = float(self.context.get("last_help_pt", 0))
        rcd_num = int(self.qrc.get('rcd_num', 0))
        rcd_cnt = 0
        try:
            userid = self.current_user["userid"]
            if last_help_pt <= 0.0:
                query = {"post_userid":userid}
            else:
                query = {"post_userid":userid,"posttime":{"$lt":last_help_pt}}
            cursor = self.application.db['permanent_help'].find(query)
            cursor.sort("posttime",-1).limit(rcd_num)
            helpdata = []
            while (yield cursor.fetch_next):
                dataline = cursor.next_object()
                del dataline['_id']
                dataline['post_datetime'] = datetime.fromtimestamp(dataline['posttime']).strftime("%Y/%m/%d %H:%M:%S")
                if 'expiretime' in dataline and dataline['expiretime'] < now_tm:
                    dataline['state'] = 2 
                helpdata.append(dataline)
                rcd_cnt += 1
            if helpdata:
                self.qrc["last_help_pt"] = helpdata[-1].get('posttime',0)
            else:
                self.qrc['last_help_pt'] = last_help_pt;
            self.qrc['rcd_num'] = rcd_cnt
            response  = {}
            response['resp_qrc'] = self.qrc
            response['resp'] = helpdata
            self.write(response)
        except Exception as e:
            self.write({"errcode":50000,"errmsg":"server internal error"})
    

class DoneHelpGetAPIHandler(APIBaseHandler):

    r"""
        @url:/resource/DoneHelpResource/get/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        last_help_pt = float(self.context.get("last_help_pt", 0.0))
        rcd_num = int(self.qrc.get("rcd_num",0))
        rcd_cnt = 0
        try:
            userid = self.current_user['userid'] 
            if last_help_pt <= 0.0:
                query = {"do_userid":userid}
            else:
                query = {"do_userid":userid,"posttime":{"$lt":last_help_pt}}
            cursor = self.application.db['permanent_help'].find(query)
            cursor.sort("posttime",-1).limit(rcd_num)
            helpdata = []
            while (yield cursor.fetch_next):
                dataline = cursor.next_object()
                del dataline['_id'] 
                dataline['post_datetime'] = datetime.fromtimestamp(dataline['posttime']).strftime("%Y/%m/%d %H:%M:%S") 
                helpdata.append(dataline)
                rcd_cnt += 1
            if helpdata:
                self.qrc['last_help_pt'] = helpdata[-1].get("posttime",0)
            else:
                self.qrc['last_help_pt'] = last_help_pt;
            self.qrc['rcd_num'] = rcd_cnt
            response = {}
            response['resp_qrc'] = self.qrc
            response['resp'] = helpdata
            self.write(response)
        except Exception as e:
            self.write({"errcode":50000,"errmsg": "server internal error"})


class UserProfileGetAPIHandler(APIBaseHandler):
   
    r"""
        @url:/resource/UserProfileResource/get/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        res = {}
        res["resp_qrc"] = self.qrc
        res["resp"] = []
        profile = {}
        profile['user_contact'] = self.current_user['usercontact']
        res["resp"].append(profile)
        self.write(res)


class UserProfileUpdateAPIHandler(APIBaseHandler):

    r"""
        @url:/resource/UserProfileResource/update/?
    """
    @web.authenticated
    @gen.coroutine
    def put(self):
        updates_profile = {}
        updates_profile['usercontact'] = self.context.get("user_contact","")
        try:
            self.session["usercontact"] = updates_profile["usercontact"]
            userid = self.current_user['userid']
            yield self.application.db['user'].update({"userid":userid},{"$set":updates_profile})
            res = {}
            res["resp_qrc"] = self.qrc
            res["resp"] = []
            self.write(res)
        except Exception:
            err_res={}
            err_res["errcode"] = 50000
            err_res["errmsg"] = "server internal error"
            self.write(err_res)
        
      
        
                
