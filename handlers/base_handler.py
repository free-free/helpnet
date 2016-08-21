#-*- coding:utf-8 -*-

from tornado import web, gen


class BaseHandler(web.RequestHandler):

    def write_error(self, status_code, **kw):
        self.render("errors/" + str(status_code) + '.html')
   
    def prepare(self):
        if not self.get_cookie(self.application.settings['site_cookie_name']):
            self.set_cookie(self.application.settings['site_cookie_name'],\
                        self.application.settings['site_cookie_val'])
        if not self.get_cookie('auth'):
            self.set_cookie("auth",'0')


class AuthNeedBaseHandler(BaseHandler):

    @gen.coroutine
    def prepare(self):
        super(AuthNeedBaseHandler,self).prepare()
        session_id = self.get_secure_cookie(self.application.settings['session_cookie'],None)
        self.session = self.application.session_cache.get_session()
        yield self.session.start(session_id)
        if self.get_cookie("auth",'0') == '0':
            self.current_user = {}
        else:
            self.current_user = self.session.all()

    @gen.coroutine
    def on_finish(self):
        if hasattr(self, 'session'):
            yield self.session.end()
            self.session.cache()


