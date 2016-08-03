# coding:utf-8

from tornado import gen,web
from .base_handler import BaseHandler


class AgreementHandler(BaseHandler):
    
    r"""
        @url:/agreement
    """
    def get(self):
        self.render("agreement.html")

