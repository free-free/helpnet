#-*- coding:utf-8 -*-
from tornado import gen,web
from .base_handler import AuthNeedBaseHandler,BaseHandler


class SearchHandler(AuthNeedBaseHandler):
	@web.authenticated
	def get(self):
		pass
	@web.authenticated
	def post(self):
		pass
