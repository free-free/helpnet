# coding:utf-8
 
from tornado import gen,web
from .base_handler import BaseHandler


class PostHelpHandler(BaseHandler):
   
    @gen.coroutine
    def get(self):
        self.render("askhelp.html")
  
    @gen.coroutine
    def post(self):
        self.write("")
 



