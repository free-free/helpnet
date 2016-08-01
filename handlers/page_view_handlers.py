#coding:utf-8

from tornado import web,gen
from .base_handler import BaseHandler 


class IndexHandler(BaseHandler):
    
    @gen.coroutine
    def get(self):
        self.write("index page")
   
    @gen.coroutine
    def post(self):
        self.write("Nothing")

