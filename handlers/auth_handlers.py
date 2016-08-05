# coding:utf-8


from tornado import web
from tornado import gen
from .base_handler import BaseHandler, AuthNeedBaseHandler
from concurrent.futures import ThreadPoolExecutor
import bcrypt
from datetime import datetime
import uuid
import base64
import json


class LoginMixin(object):

    @gen.coroutine
    def signin(self, success_redirect_url):
        email = self.get_argument("_email", '')
        password = self.get_argument("_password", '')
        user_data = yield self.application.db['users'].find_one({"email": email})
        if not user_data:
            self.render("login.html")  # user not exists
            return
        hashed_password = yield self.application.executor.submit(bcrypt.hashpw, password.encode("utf-8"), user_data['hashed_password'])
        if hashed_password != user_data['hashed_password']:
            self.render("login.html")  # user password wrong
            return
        user_data['last_login_at'] = user_data['login_at']
        user_data['login_at'] = str(datetime.timestamp(datetime.now()))
        yield self.application.db['users'].update({"email": email}, {'$set': {'last_login_at': user_data['last_login_at'], 'login_at': user_data['login_at']}})
        del user_data['_id']
        del user_data['hashed_password']
        yield self.session.start()
        self.session.multi_set(user_data)
        yield self.session.save()
        self.set_secure_cookie(self.application.settings['session_cookie'], self.session.session_id)
        self.set_secure_cookie("_lgtsp", str(datetime.timestamp(datetime.now())))
        self.set_secure_cookie("_auth", "1")
        self.redirect(success_redirect_url)


class LoginHandler(AuthNeedBaseHandler, LoginMixin):
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

    @gen.coroutine
    def post(self):
        yield self.signin('/')


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
