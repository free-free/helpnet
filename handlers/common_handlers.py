#-*- coding:utf-8 -*-
from tornado import web, gen
from .base_handler import BaseHandler, AuthNeedBaseHandler
import bcrypt
from concurrent.futures import ThreadPoolExecutor
import base64
from datetime import datetime
import re

class UserSignUpMixin(object):

    @gen.coroutine
    def check_email_existence(self, email):
        CHECK_RESPONSE_FORMAT['type'] = 1
        CHECK_RESPONSE_FORMAT['data']['check_field'] = "email"
        if not email:
            email_indb = yield self.application.db['users'].find_one({"email": email}, {"email": 1})
            if email_indb:
                CHECK_RESPONSE_FORMAT['data']['exist'] = 1
                self.write(CHECK_RESPONSE_FORMAT)
            else:
                CHECK_RESPONSE_FORMAT['data']['exist'] = 0
                self.write(CEHCK_RESPONSE_FORMAT)
        else:
            CHECK_RESPONSE_FORMAT['data']['exist'] = 0
            self.write(CEHCK_RESPONSE_FORMAT)
        self.finish()

    @gen.coroutine
    def signup(self, failed_url, success_url):
        email_regx = r'^[a-z0-9A-Z_-]+@[a-zA-Z0-9_-]+(.[a-z0-9A-Z_-]+)+$'
        password = self.get_argument("_password", '')
        email = self.get_argument("_email", '')
        if not re.match(email_regx, email):
            self.render("register_index.html")
        elif len(password) < 6:
            self.render("register_index.html")
        else:
            user_data = yield self.application.db['users'].find_one({"email": email}, {"email": 1})
            if user_data:
                self.render("register_index.html")  # email registered
                return
            email_split = re.split(r'[@.]', email)
            username = email_split[0]
            user_data = yield self.application.db['users'].find_one({"username": username}, {"username": 1})
            if user_data:
                username = email_split[0] + email_split[1]
            hashed_password = yield self.application.executor.submit(bcrypt.hashpw, password.encode('utf-8'), bcrypt.gensalt())
            now_timestamp = str(datetime.timestamp(datetime.now()))
            user_data = {
                "username": username,
                "hashed_password": hashed_password,
                "email": email,
                "create_at": now_timestamp,
                "login_at": now_timestamp,
                "last_login_at": now_timestamp,
            }
            yield self.application.db['users'].insert(user_data)
            del user_data['_id']
            self.session.multi_set(user_data)
            yield self.session.save()
            self.set_secure_cookie(self.application.settings['session_cookie'], self.session.session_id)
            self.set_secure_cookie("_auth", "1")
            self.set_secure_cookie("_lgtsp", now_timestamp)
            self.redirect(success_url)
