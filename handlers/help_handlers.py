# coding:utf-8


from tornado import gen,web
from .base_handler import BaseHandler,AuthNeedBaseHandler
import shortuuid
import time

class HelpListHandler(AuthNeedBaseHandler):
     
    r'''
     @url: /
    ''' 
    @gen.coroutine
    def get(self):
        self.render("helplist.html")


class PostHelpHandler(AuthNeedBaseHandler):
   
    r"""
        @url:/askhelp
    """
    @gen.coroutine
    def get(self):
        self.render("askhelp.html")
  
    @gen.coroutine
    def post(self):
        helpinfo = {}
        helpinfo['helpid'] = shortuuid.uuid()
        helpinfo['helpcontent'] = self.get_argument("help_content")
        helpinfo['helpremark'] = self.get_argument("help_remark")
        helpinfo['helpreward'] = self.get_argument("help_reward")
        helpinfo['posttime'] = time.time()
        helpinfo['finishtime'] = 0
        helpinfo['lifetime'] = 3600
        helpinfo['helpstate'] = 0
        helpinfo['ispay'] = 0
        helpinfo['location'] = []
        helpinfo['location'][0] = self.get_argument("longitude")
        helpinfo['location'][1] = self.get_argument("latitude")
        helpinfo['address'] = self.get_argument("address",None) \
            or self.current_user['address']
        helpinfo['locprec'] = 0.0
        helpinfo['post_username'] = self.current_user['username']
        helpinfo['post_userid'] = self.current_user['userid']
        helpinfo['post_userheadimgurl'] = self.current_user['headimgurl']
        helpcontact = self.get_argument("help_contact",None) \
            or self.current_user['usercontact']
        helpinfo['post_usercontact'] = helpcontact 
        try:
            help_exist = yield self.application.db['help'].find_one({'helpid':helpinfo['helpid']},{"helpid":1})
            if not help_exist:
                response = yield self.application.db['help'].insert(helpinfo)
                if response:
                    self.write("askhelp_success.html")
                else:
                    self.set_status(500)
                    self.render("errors/500.html")
            else:
                self.set_status(500)
                self.render("errors/500.html")
        except Exception:
            self.set_status(500)
            self.render("errors/500.html")


class GetHelpHandler(AuthNeedBaseHandler):
   
    r"""
        @url:/gethelp/([0-9a-zA-Z]+)/?
    """
    @gen.coroutine
    def post(self,helpid):
        try:
            helpdata = yield self.application.db['help'].find_one({"helpid":helpid})
            if not helpdata:
                self.set_status(500)
                self.render("errors/500.html")
                return 
            if helpdata['helpstate'] == 0:
                helpdata['helpstate'] = 1
                helpdata['get_userid'] = self.current_user['userid']
                helpdata['get_username'] = self.current_user['username']
                helpdata['get_userheadimgurl'] = self.current_user['headimgurl']
                helpdata['finishtime'] = time.time()
                self.render("gethelp_success.html") 
            elif helpdata['helpstate'] == 1:
                self.render("gethelp_failed.html",reason="already solved by others")
            else:
                self.render("gethelp_failed.html",readon="expired")
        except Exception:
            self.set_status(500)
            self.render("errors/500.html")


class HelpDetailHandler(AuthNeedBaseHandler):

    r"""
        @url:/help/([0-9a-zA-Z]+)/?
    """
    @gen.coroutine
    def get(self, helpid):
        try:
            helpdata = yield self.application.db['help'].find_one({"helpid":helpid})
            if helpdata:
                del helpdata['_id']
                self.write(helpdata)
            else:
                self.render("helpdetail.html")
                #self.set_status(404)
                #self.render("errors/404.html")
        except Exception:
            self.set_status(500)
            self.render("errors/500.html")
