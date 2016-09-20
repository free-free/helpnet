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
        try:
            criteria = {"userid":self.current_user['userid']};
            projects = {"_id":0,"username":1,"headimgurl":1,"help_cnt":1}
            userdata = yield self.application.db['user'].find_one(criteria, projects)
            self.render("UserHome/index.html", userdata=userdata)
        except Exception as e:
            print(e)
            self.set_status(500)
            self.render("errors/500.html")


class UserPostedHelpHandler(AuthNeedBaseHandler):
   
    r"""
        @url:/user/postedhelp/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        try:
            criteria = {"userid":self.current_user['userid']};
            projects = {"_id":0,"username":1,"headimgurl":1,"help_cnt":1}
            userdata = yield self.application.db['user'].find_one(criteria, projects)
            self.render("UserHome/postedhelp.html", userdata=userdata)
        except Exception:
            self.set_status(500)
            self.render("errors/500.html");


class UserDoneHelpHandler(AuthNeedBaseHandler):
  
    r"""
        @url:/user/donehelp/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        try:
            criteria = {"userid":self.current_user['userid']};
            projects = {"_id":0,"username":1,"headimgurl":1,"help_cnt":1}
            userdata = yield self.application.db['user'].find_one(criteria, projects)
            self.render("UserHome/donehelp.html", userdata=userdata)
        except Exception:
            self.set_status(500)
            self.render("errors/500.html")


class UserProfileHandler(AuthNeedBaseHandler):
    r"""
        @url:/user/profile/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        self.render("userprofile.html")

    
          
