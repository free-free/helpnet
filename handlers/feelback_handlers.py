# coding:utf-8

import time

from tornado import web, gen

from .base_handler import AuthNeedBaseHandler



class FeelbackHandler(AuthNeedBaseHandler):
    
    r"""
        @url: /feelback/
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        self.render("Feelback/index.html")


    @web.authenticated
    @gen.coroutine
    def post(self):
        fb_text = self.get_argument("fb_text")
        if not fb_text.strip():
            self.set_status(403)
            self.render("Feelback/result.html", result_text="反馈意见不能为空!", result_code=-1)
            return 
        fb_data = {}
        fb_data['fb_text'] = fb_text
        fb_data['userid'] = self.current_user['userid']
        fb_data['username'] = self.current_user['username']
        fb_data['create_at'] = time.time()
        fb_data['is_read'] = 0
        try:
            yield self.application.db['feelback'].insert(fb_data)
            self.render("Feelback/result.html", result_text="谢谢反馈!", result_code=0)
        except Exception as e:
            self.set_status(500)
            self.render("Feelback/result.html", result_text="反馈意见失败，请重试!", result_code=-1)


