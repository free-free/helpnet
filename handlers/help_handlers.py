# coding:utf-8


from tornado import gen,web
from .base_handler import BaseHandler
import shortuuid
import time

class HelpListHandler(BaseHandler):
     
    r'''
     @url: /
    ''' 
    @gen.coroutine
    def get(self):
        self.render("map.html")


class PostHelpHandler(BaseHandler):
   
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
        helpinfo['locprec'] = 0.0
        helpinfo['post_username'] = self.current_user['username']
        helpinfo['post_userid'] = self.current_user['userid']
        helpinfo['post_userheadimgurl'] = self.current_user['headimgurl']
        helpcontact = self.get_argument("help_contact",None) \
            or self.current_user['usercontact']
        helpinfo['post_usercontact'] = helpcontact 
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
	
       
        


class HelpItemDetailHandler(BaseHandler):

    r"""
        @url:/help/([0-9a-zA-Z]+)/?
    """
    @gen.coroutine
    def get(self, help_id):
        help_info = yield self.application.db['help'].find_one({"helpid":help_id})
        if help_info:
            del help_info['_id']
            self.write(help_info)
        self.render("helpdetail.html")
        #else:
        #    self.set_status(404)
        #    self.render("errors/404.html")
