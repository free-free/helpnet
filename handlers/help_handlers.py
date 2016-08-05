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
   
    r"""
        @url:/askhelp
    """
    @gen.coroutine
    def get(self):
        self.render("askhelp.html")
  
    @gen.coroutine
    def post(self):
        self.write("")


class HelpHandler(BaseHandler):

    r"""
        @url:/help/([0-9a-zA-Z]+)/?
    """
    @gen.coroutine
    def get(self, help_id):
        help_info = yield self.application.db['help'].find_one({"help_id":help_id})
        if help_info:
            del help_info['_id']
            self.write(help_info)
        else:
            self.set_status(404)
            self.render("errors/404.html")
