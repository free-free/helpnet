#!/usr/bin/env python3.5

import os

from celery import Celery
from tornado import web
from tornado import ioloop
import tornado.options
import tornado.autoreload
from tornado.options import options, define
from tornasess import SessionCacheFactory
from tornado_hbredis import TornadoHBRedis
from motor.motor_tornado import MotorClient
import concurrent.futures

from handlers.user_handlers import *
from handlers.auth_handlers import *
from handlers.search_handlers import *
from handlers.wxcallback_handlers import *
from handlers.help_handlers import *
from handlers.feelback_handlers import *
from handlers.check_signature_handlers import CheckSignatureHandler
from handlers.api_handlers import *
from config import config

class DefaultHandler(web.RequestHandler):

    def write_error(self, status_code, **kw):
        self.set_status(status_code)
        self.render("errors/" + str(status_code) + ".html")

    def get(self):
        self.set_status(404)
        self.render("errors/404.html")
        
    def post(self):
        self.set_status(404)
        self.render("errors/404.html")

    def delete(self):
        self.set_status(404)
        self.render("errors/404.html")

    def put(self):
        self.set_status(404)
        self.render("errors/404.html")
        



class Application(web.Application):

    def __init__(self):
        settings = {
            'template_path': os.path.join(os.path.dirname(__file__), 'views'),
            'static_path': os.path.join(os.path.dirname(__file__), 'static'),
            'login_url': '/login/',
            'cookie_secret': 'MmUyZmU2NmIyNDM4NDc4YWE4OTNiODUzMjhhZTgzM2U3NDU5OGUwNzNlODY0ODI5ODM1MGNmNjcxZmU5M2FjNg==',
            #'xsrf_cookies': True,
            'default_handler_class': DefaultHandler,
            'session_cookie_name': '_huzhugc_sess',
            'site_cookie_name':'_huzhugc_com',
            'site_cookie_val':'c88e90e3a7390246a53cef4bf3c145f0ad3215cc',
            'public_appid':config['public_appid'],
            'public_secret':config['public_secret'],
            'wx_state_key':'huzhugc.com',
            'wx_callback_token':'huzhugctoken',
            'debug':True,
        }

        handlers = [
            (r'/', HelpListHandler),
            (r'/logout/?', LogoutHandler),
            (r'/wxcallback/?', WXCallbackHandler),
            #(r'/wxcallback/?', CheckSignatureHandler),
            (r'/login/?', LoginHandler),
            (r'/wxpubloginredirect/?', WXPubLoginRedirectHandler),
            (r'/wxpublogin/?', WXPubLoginHandler),
            (r'/posthelp/?', PostHelpHandler),
            (r'/dohelp/([0-9a-zA-Z]+)/?', DoHelpHandler),
            (r'/search/?', SearchHandler), 
            (r'/user/?', UserHomeHandler),
            (r'/feelback/?', FeelbackHandler),
            (r'/user/postedhelp/?', UserPostedHelpHandler),
            (r'/user/donehelp/?', UserDoneHelpHandler),
            (r'/user/profile/?', UserProfileHandler),
            (r'/resource/WXJSApiResource/get/?', WeixinJSApiAPIHandler),
            (r'/resource/WXQRCodeResource/get/?', WeixinQRCodeGetAPIHandler),
            (r'/resource/UpdatesHelpResource/get/?', UpdatesHelpGetAPIHandler),
            (r'/resource/PostedHelpResource/get/?', PostedHelpGetAPIHandler),
            (r'/resource/DoneHelpResource/get/?', DoneHelpGetAPIHandler),
            (r'/resource/HelpResource/delete/?', HelpResourceAPIHandler),
            (r'/resource/UserPositionResource/update/?', UserPositionUpdateAPIHandler),
            (r'/resource/UserProfileResource/get/?', UserProfileGetAPIHandler),
            (r'/resource/UserProfileResource/update/?', UserProfileUpdateAPIHandler),
        ]
        super(Application, self).__init__(handlers=handlers, **settings)
        conn = MotorClient(config['mongodb']['host'], config['mongodb']['port'])
        self.db = conn['hnet']
        #self.executor = concurrent.futures.ThreadPoolExecutor(2)
        self.session_cache = SessionCacheFactory('redis')
        self.cache = TornadoHBRedis(config['redis']['host'], config['redis']['port'], bytes_decode=True)
        self.task = Celery()
        self.task.config_from_object("celeryconfig")

define("port", default=8000, help="server port", type=int)
if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    loop = ioloop.IOLoop.current()
    tornado.autoreload.start(loop)
    loop.start()
