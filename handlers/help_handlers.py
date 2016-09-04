# coding:utf-8

import time
from datetime import datetime

import shortuuid
from tornado import gen,web

from .base_handler import BaseHandler,AuthNeedBaseHandler


class HelpListHandler(AuthNeedBaseHandler):
     
    r"""
     @url: /
    """
    #@web.authenticated
    @gen.coroutine
    def get(self):
        self.render("helplist.html")


class AskHelpHandler(AuthNeedBaseHandler):
   
    r"""
        @url:/askhelp
    """
    #@web.authenticated
    @gen.coroutine
    def get(self):
        self.render("askhelp.html")
  
    #@web.authenticated
    @gen.coroutine
    def post(self):
        tm = str(time.time())
        helpdata = {}
        helpdata['helpid'] = shortuuid.uuid()
        helpdata['help_content'] = self.get_argument("help_content")
        helpdata['help_price'] = self.get_argument("help_price")
        helpdata['location'] = []
        helpdata['location'].append(self.get_argument("help_lng","") \
            or self.current_user['location'][0]);
        helpdata['location'].append(self.get_argument("help_lat","") \
            or self.current_user['location'][1]);
        helpdata['help_address'] = self.get_argument("help_address",None) \
            or self.current_user.get('address','')
        helpdata['locprec'] = 0.0
        helpdata['post_username'] = self.current_user['username']
        helpdata['post_userid'] = self.current_user['userid']
        helpdata['post_userheadimgurl'] = self.current_user['headimgurl']
        helpcontact = self.get_argument("post_usercontact",None) \
            or self.current_user['usercontact']
        helpdata['post_usercontact'] = helpcontact 
        helpdata['post_usercontact_means'] = self.get_argument("post_usercontact_means")
        helpdata['posttime'] = tm
        helpdata['finishtime'] = tm
        if self.get_argument("help_expiretime"): 
            helpdata['expiretime'] = tm + self.get_argument("help_expiretime")
        else:
            helpdata['expiretime'] = 0
        helpdata['help_state'] = 0
        helpdata['ispay'] = 0
        try:
            help_exist = yield self.application.db['help_order'].find_one({'helpid':helpdata['helpid']},{"helpid":1})
            if not help_exist:
                yield self.application.db['help_order'].insert(helpdata)
                self.write("askhelp_success.html")
            else:
                self.set_status(500)
                self.render("errors/500.html")
        except Exception:
            self.set_status(500)
            self.render("errors/500.html")


class DoHelpHandler(AuthNeedBaseHandler):
   


    r"""
        @url:/dohelp/([0-9a-zA-Z]+)/?
    """
   # @web.authenticated
    @gen.coroutine
    def get(self, helpid):
        self.render("dohelp.html")
        return 


   # @web.authenticated
    @gen.coroutine
    def post(self, helpid):
        do_usercontact = self.get_argument("do_usercontact")
        do_usercontact_means = self.get_argument("do_usercontact_means")
        try:
            helpdata = yield self.application.db['help'].find_one({"helpid":helpid})
            if not helpdata:
                self.set_status(403)
                self.render("errors/403.html")
                return 
            if helpdata['helpstate'] == 0:
                helpdata['helpstate'] = 1
                helpdata['do_userid'] = self.current_user['userid']
                helpdata['do_username'] = self.current_user['username']
                helpdata['do_userheadimgurl'] = self.current_user['headimgurl']
                helpdata['finishtime'] = datetime.timestamp(datetime.now())
                self.write("dohelp_result.html") 
            elif helpdata['helpstate'] == 1:
                self.render("dohelp_result.html",reason="already solved by others")
            else:
                self.render("dohelp_result.html",readon="expired")
        except Exception:
            self.set_status(500)
            self.render("errors/500.html")


class HelpDetailHandler(AuthNeedBaseHandler):

    r"""
        @url:/help/([0-9a-zA-Z]+)/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self, helpid):
        self.render("helpdetail.html",);
        return 
        try:
            helpdata = yield self.application.db['help'].find_one({"helpid":helpid})
            if helpdata:
                del helpdata['_id']
                self.render('helpdetail.html', data=helpdata)
            else:
                self.set_status(404)
                self.render("errors/404.html")
        except Exception:
            self.set_status(500)
            self.render("errors/500.html")
