#-*- coding:utf-8 -*-

from tornado import web
from tornado import gen
from .base_handler import BaseHandler, AuthNeedBaseHandler
from concurrent.futures import ThreadPoolExecutor
import bcrypt
from datetime import datetime
import uuid
import base64

class UserHomeHandler(AuthNeedBaseHandler):
    r"""
        @url:/([a-zA-Z0-9]+)/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self, username):
        user_data = yield self.application.db['user'].find_one({"username": username})
        if not user_data:
            self.set_status(404)
            self.write("Page Not Found!")
            self.finish()
        else:
            del user_data['_id']
            self.write(user_data)


class UserSettingsHandler(AuthNeedBaseHandler):
    r"""
        @url:/settings
    """
    @web.authenticated
    def get(self):
        self.write("settings page")
