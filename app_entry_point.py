#!/usr/bin/env python3.5

from tornado import web
from tornado import ioloop
import tornado.options
import tornado.autoreload
from tornado.options import options, define

from handlers.user_handlers import *
from handlers.auth_handlers import *
from handlers.search_handlers import *
from handlers.callback_handlers import *
from handlers.help_handlers import *
from handlers.check_signature_handlers import CheckSignatureHandler
from handlers.about_handler import AboutHandler
from handlers.document_handler import DocumentHandler
from handlers.agreement_handler import AgreementHandler
from handlers.api_handlers import *


from tornado_session import SessionCacheFactory
from tornado_hbredis import TornadoHBRedis
import os
from motor.motor_tornado import MotorClient
import concurrent.futures


class DefaultHandler(web.RequestHandler):

    def write_error(self, status_code, **kw):
        self.set_status(status_code)
        self.render("errors/" + str(status_code) + ".html")

    def get(self):
        self.set_status(404)
        self.render("errors/404.html")



class Application(web.Application):

    def __init__(self):

        settings = {
            'template_path': os.path.join(os.path.dirname(__file__), 'views'),
            'static_path': os.path.join(os.path.dirname(__file__), 'assets'),
            'login_url': '/login',
            'cookie_secret': 'MmUyZmU2NmIyNDM4NDc4YWE4OTNiODUzMjhhZTgzM2U3NDU5OGUwNzNlODY0ODI5ODM1MGNmNjcxZmU5M2FjNg==',
            #'xsrf_cookies': True,
            'default_handler_class': DefaultHandler,
            'session_cookie': '_helpnet_sess'
        }

        handlers = [
            (r'/', HelpListHandler),
            (r'/askhelp/?', PostHelpHandler),
            (r'/logout/?', LogoutHandler),
            (r'/callback', CallbackHandler),
            (r'/login/?', LoginHandler),
            (r'/search/?', SearchHandler),
            (r'/settings/?', UserSettingsHandler),
            (r'/about/?', AboutHandler), 
            (r'/document/?', DocumentHandler),
            (r'/agreement/?', AgreementHandler),
            (r'/resources/WeixinQRCodeResource/get/?',WeixinQRCodeAPIHandler),
            (r'/help/([0-9a-zA-Z]+)/?', HelpHandler),
            (r'/([a-zA-Z0-9]+)/?', UserHomeHandler),
        ]
        super(Application, self).__init__(handlers=handlers, **settings)
        conn = MotorClient('localhost', 4000)
        self.db = conn['fsp']
        self.executor = concurrent.futures.ThreadPoolExecutor(2)
        self.session_cache = SessionCacheFactory('redis', 'localhost', 6379)
        self.cache = TornadoHBRedis("localhost",6379)

define("port", default=8000, help="server port", type=int)
if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    loop = ioloop.IOLoop.current()
    tornado.autoreload.start(loop)
    loop.start()
