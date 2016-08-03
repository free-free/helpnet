# coding:utf-8
 
from tornado import gen,web
from .base_hander import BaseHandler


class PostHelpHandler(BaseHandler):
   
    @gen.coroutine
    def get(self):
        self.render("index.html")
  
    @gen.coroutine
    def post(self):
        self.render("index.html")
 



