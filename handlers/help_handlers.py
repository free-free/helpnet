# coding:utf-8


from tornado import gen,web
from .base_handler import BaseHandler


class HelpListHandler(BaseHandler):
     
    r'''
     @url: /
    ''' 
    @gen.coroutine
    def get(self):
        self.render("helplist.html")


class PostHelpHandler(BaseHandler):
   
    @gen.coroutine
    def get(self):
        self.render("askhelp.html")
  
    @gen.coroutine
    def post(self):
        self.write("")




