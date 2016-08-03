# coding:utf-8


from tornado import gen,web
from .base_handler import BaseHandler


class AboutHandler(BaseHandler):
 
    r"""
        @url:/about/?
    """
    def get(self):
        self.render("about.html")



