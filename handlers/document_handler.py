# coding;utf-8

from tornado import gen,web
from .base_handler import BaseHandler




class DocumentHandler(BaseHandler):
 
    r"""
        @url:/document/?
    """
    def get(self):
        self.render("document.html")


