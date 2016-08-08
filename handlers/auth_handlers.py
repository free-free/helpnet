# coding:utf-8


from tornado import web
from tornado import gen
from .base_handler import BaseHandler, AuthNeedBaseHandler
from . import send_async_request,generate_state,certify_state
from concurrent.futures import ThreadPoolExecutor
import bcrypt
from datetime import datetime
import uuid
import base64
import json
import time


class LoginHandler(AuthNeedBaseHandler):
    r"""
        @url:/login
    """
    @gen.coroutine
    def prepare(self):
        yield super(LoginHandler, self).prepare()
        if self.current_user:
            self.redirect('/')

    @gen.coroutine
    def get(self):
        self.render('login.html')



class WXSubscribeLoginHandler(AuthNeedBaseHandler):

    r"""
        @url:/wxsubslogin/?
    """
    @gen.coroutine
    def prepare(self):
        yield super(WXSubscribeLoginHandler,self).prepare()
        if current_user:
            self.redirect('/')
 
    @gen.coroutine
    def get(self):
        state = self.get_argument("state", "")
        code  = self.get_argument("code","")
        if not code or not certify_state("deude",state):
            self.set_statue(500)
            self.render("error/500.html")
            return 
        ackurl = "https://api.weixin.qq.com/sns/oauth2/access_token? \
            appid={0}&secret={1}&code={2}&grant_type=authorization_code"
        ackurl.format(self.application.settings['public_appid'],\
                      self.application.settings['public_secret'],\
                      code)
        try: 
            response = yield send_async_request(ackurl)
            response = response.body.decode("utf-8")
            openid = response['openid']
            #check user existence
            userdata = yield self.application.db['user'].find({"userid":openid})
            if not userdata:
                self.redirect('/login')
                return   
            del userdata['_id']
            userdata['longitude'] = userdata['location'][0]
            userdata['latitude'] = userdata['location'][1]
            self.session.multi_set(userdata)
            yield self.session.save(7200)
            self.set_cookie(self.application.settings['session_cookie'],self.session.session_id)
            self.set_cookie("auth",'1')
            self.redirect('/')
        except Exception:
            self.redirect('/login')
            

class WXAuthCallbackLoginHandler(AuthNeedBaseHandler):
    
    r"""
        @url:/wxauthlogin/?
    """
    @gen.coroutine
    def prepare(self):
        yield super(WXAuthCallbackLoginHandler,self).prepare()
        if self.current_user:
            self.redirect('/')
   
    @gen.coroutine
    def get(self):
        state = self.get_argument("state","")
        code = self.get_argument("code","")
        if not code or not certify_state("dheuide",state):
            # weixin reject to authentication,redirect to login page
            self.redirect('/login')
            return 
        ackurl = "https://api.weixin.qq.com/sns/oauth2/access_token? \
            appid={0}&secret={1}&code={2}&grant_type=authorization_code"
        ackurl.format(WEB_APPID,WEB_SECRET,code)
        try:
            response = yield send_async_request(ackurl)
            response = response.body.decode("utf-8")
            openid = response['openid']
            #check user existence
            userdata = yield self.application.db['user'].find({"userid":openid})
            if not userdata:
                userdataurl = "https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}"
                userdataurl.format(response['access_token'],openid)
                response = yield send_async_request(userdataurl)
                userdata = response.body.decode('utf-8') 
                userdata['createtime'] = time.time()
                userdata['subscribe'] = 0
                userdata['userid'] = userdata.pop('openid')
                userdata['username'] = userdata.pop('nickname')
                del userdata['privilege']
                yield self.application.db['user'].insert(userdata)
            del userdata['_id']
            userdata['longitude'] = userdata['location'][0]
            userdata['latitude'] = userdata['location'][1]
            self.session.multi_set(userdata)
            yield self.session.save(7200)
            self.set_cookie("auth",'1')
            self.set_cookie(self.application.settings['session_cookie'],self.session.session_id)
            self.redirect('/')
        except Exception:
            self.redirect('/login')
            self.finish()


class LogoutHandler(AuthNeedBaseHandler):
    r"""
        @url:/logout
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        self.clear_all_cookies()
        yield self.session.destroy()
        self.redirect('/')
