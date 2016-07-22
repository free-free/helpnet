#-*- coding:utf-8 -*-

from tornado import web, gen


class BaseHandler(web.RequestHandler):

    def write_error(self, status_code, **kw):
        self.render("errors/" + str(status_code) + '.html')

class AuthNeedBaseHandler(BaseHandler):

    @gen.coroutine
    def prepare(self):
        session_id = self.get_secure_cookie(self.application.settings['session_cookie'],None)
        self.session = self.application.session_cache.get_session()
        yield self.session.start(session_id)
        self.current_user = self.session.all()

    def on_finish(self):
        if hasattr(self, 'session'):
            self.session.cache()


