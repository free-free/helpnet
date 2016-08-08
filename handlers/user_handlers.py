#-*- coding:utf-8 -*-

from datetime import datetime
import uuid
import base64

from tornado import web
from tornado import gen
from concurrent.futures import ThreadPoolExecutor
import bcrypt

from .base_handler import BaseHandler, AuthNeedBaseHandler


class UserHomeHandler(AuthNeedBaseHandler):
    r"""
        @url:/user/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        self.render("userhome.html")


class UserPostHelpListHandler(AuthNeedBaseHandler):
   
    r"""
        @url:/user/posthelp/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        self.render("userposthelp.html")


class UserGetHelpListHandler(AuthNeedBaseHandler):
  
    r"""
        @url:/user/gethelp/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        self.render("usergethelp.html")


class UserProfileHandler(AuthNeedBaseHandler):
    r"""
        @url:/user/profile/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        self.render("userprofile.html")

    
          
