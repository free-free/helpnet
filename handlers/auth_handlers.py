# coding:utf-8


from datetime import datetime
import uuid
import base64
import json
import time

from tornado import gen,web

from .base_handler import BaseHandler, AuthNeedBaseHandler
from . import send_async_request,generate_state,certify_state


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


class WXPubLoginRedirectHandler(BaseHandler):
    
    r"""
        @url:/wxpubloginredirect/?
    """
    @gen.coroutine
    def get(self):
        state = generate_state(self.application.settings['wx_state_key'],120)
        auth_url = "https://open.weixin.qq.com/connect/oauth2/authorize?\
appid={0}&redirect_uri={1}&response_type=code&scope=snsapi_base&state={2}#wechat_redirect"
        auth_url = auth_url.format(self.application.settings['public_appid'],
            "http://www.huzhugc.com/wxpublogin/",state)
        self.redirect(auth_url)

 
class WXPubLoginHandler(AuthNeedBaseHandler):

    r"""
        @url:/wxpublogin/?
    """
 
    @gen.coroutine
    def get(self):
        state = self.get_argument("state")
        code  = self.get_argument("code")
        if not code or not certify_state(self.application.settings['wx_state_key'],state):
            self.redirect('/login')
            return 
        code_url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}\
&secret={1}&code={2}&grant_type=authorization_code"
        code_url = code_url.format(self.application.settings['public_appid'],
            self.application.settings['public_secret'],code)
        try: 
            response = yield send_async_request(code_url)
            response = json.loads(response.body.decode("utf-8"))
            openid = response['openid']
            #check user existence
            userdata = yield self.application.db['user'].find_one({"userid":openid})
            if not userdata:
                self.redirect('/login')
                return    
            del userdata['_id']
            self.session.multi_set(userdata)
            self.set_cookie("auth",'1')
            self.redirect('/')
        except Exception as e:
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
            userdata = yield self.application.db['user'].find_one({"userid":openid})
            if not userdata:
                userdataurl = "https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}"
                userdataurl = userdataurl.format(response['access_token'],openid)
                response = yield send_async_request(userdataurl)
                userdata = response.body.decode('utf-8') 
                userdata['createtime'] = time.time()
                userdata['subscribe'] = 0
                userdata['userid'] = userdata.pop('openid')
                userdata['username'] = userdata.pop('nickname')
                del userdata['privilege']
                yield self.application.db['user'].insert(userdata)
            del userdata['_id']
            self.session.multi_set(userdata)
            self.set_cookie("auth",'1')
            self.set_cookie(self.application.settings['session_cookie'],self.session.session_id)
            self.redirect('/')
        except Exception:
            self.redirect('/login')


class LogoutHandler(AuthNeedBaseHandler):
    r"""
        @url:/logout
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        self.clear_all_cookies()
        try:
            yield self.session.destroy()
        except Exception:
            self.set_status(500)
            self.render("errors/500.html")
        self.redirect('/login/')
