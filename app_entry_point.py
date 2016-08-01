#!/usr/bin/env python3.5

from tornado import web
from tornado import ioloop
import tornado.options
from tornado.options import options, define

from handlers.user_handlers import *
from handlers.resource_api_handlers import *
from handlers.search_handlers import *
from handlers.page_view_handlers import *
from handlers.callback_handlers import *
from tornado_session import SessionCacheFactory
import os
from motor import MotorClient
import concurrent.futures


class DefaultHandler(web.RequestHandler):

    def write_error(self, status_code, **kw):
        self.render("errors/" + str(status_code) + ".html")

    def get(self):
        self.render("errors/404.html")

    def post(self):
        self.render("errors/404.html")


class Application(web.Application):

    def __init__(self):

        settings = {
            'template_path': os.path.join(os.path.dirname(__file__), 'views'),
            'static_path': os.path.join(os.path.dirname(__file__), 'static'),
            'login_url': '/login',
            'cookie_secret': 'MmUyZmU2NmIyNDM4NDc4YWE4OTNiODUzMjhhZTgzM2U3NDU5OGUwNzNlODY0ODI5ODM1MGNmNjcxZmU5M2FjNg==',
            'xsrf_cookies': True,
            'default_handler_class': DefaultHandler,
            'session_cookie': '_helpnet_sess'
        }

        handlers = [
            (r'/', IndexHandler),
            (r'/logout/?', UserLogoutHandler),
            (r'/callback', CallbackHandler),
            (r'/login/?', UserLoginHandler),
            (r'/search/?', SearchHandler),
            (r'/settings/?', UserSettingsHandler),
            (r'/([a-zA-Z0-9]+)/?', UserHomeHandler),
            (r'/resource/UserSettingsResource/update/?',ResourceUserSettingsResourceUpdateHandler),
            (r'/resource/UserSettingsResource/get/?',ResourceUserSettingsResourceGetHandler),
        ]
        super(Application, self).__init__(handlers=handlers, **settings)
        conn = MotorClient('localhost', 27017)
        self.db = conn['fsp']
        self.executor = concurrent.futures.ThreadPoolExecutor(2)
        self.session_cache = SessionCacheFactory('redis', 'localhost', 6379)

define("port", default=8000, help="server port", type=int)
if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    ioloop.IOLoop.current().start()
