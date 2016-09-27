# coding:utf-8

import time
from datetime import datetime
import re

import shortuuid
from tornado import gen,web

from .base_handler import BaseHandler,AuthNeedBaseHandler


class HelpListHandler(AuthNeedBaseHandler):
     
    r"""
     @url: /
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        self.render("Help/List/index.html")


class PostHelpHandler(AuthNeedBaseHandler):
   
    r"""
        @url:/posthelp/
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        self.render("Help/Post/index.html", defaults={})
  
    @web.authenticated
    @gen.coroutine
    def post(self):
        tm =  time.time()
        helpdata = {}
        helpdata['helpid'] = shortuuid.uuid()
        helpdata['content'] = self.get_argument("help_content")
        helpdata['price'] = self.get_argument("help_price")
        helpdata['location'] = []
        helpdata['location'].append(self.get_argument("help_lng", \
            self.current_user['location'][0])) 
        helpdata['location'].append(self.get_argument("help_lat", \
            self.current_user['location'][1]))
        helpdata['location'][0] = float(helpdata['location'][0])
        helpdata['location'][1] = float(helpdata['location'][1])
        helpdata['address'] = self.get_argument("help_address", \
            self.current_user.get("address", ""))
        helpdata['post_username'] = self.current_user['username']
        helpdata['post_userid'] = self.current_user['userid']
        helpdata['post_userheadimgurl'] = self.current_user['headimgurl']
        helpcontact = self.get_argument("post_usercontact", \
            self.current_user.get('usercontact',""))
        helpdata['post_usercontact'] = helpcontact 
        helpdata['post_usercontact_means'] = self.get_argument("post_usercontact_means")
        helpdata['posttime'] = tm
        helpdata['finishtime'] = 0
        if self.get_argument("help_expiretime"): 
            helpdata['expiretime'] = tm + float(self.get_argument("help_expiretime"))*60
        helpdata['state'] = 0
        try:
            help_exist = yield self.application.db['permanent_help'].find_one({'helpid':helpdata['helpid']},{"helpid":1})
            if not help_exist:
                yield self.application.db['permanent_help'].insert(helpdata)
                yield self.application.db['updates_help'].insert(helpdata);
                criteria = {"userid":self.current_user["userid"]}
                modifier = {"$inc":{"help_cnt.posted_help_num":1}}
                yield self.application.db['user'].update(criteria, modifier ,upsert=True);
                self.redirect("/")
            else:
                defaults = {}
                defaults['help_content'] = helpdata['content']
                defaults['help_price'] = helpdata['price']
                defaults['post_usercontact'] = helpdata['post_usercontact']
                defaults['post_usercontact_means'] = helpdata['post_usercontact_means']
                defaults['help_address'] = helpdata['address']
                defaults['help_lng'] = helpdata['location'][0]
                defaults['help_lat'] = helpdata['location'][1]
                defaults['help_expiretime'] = self.get_argument("help_expiretime", '')
                defaults['toptip'] = True
                self.render("Help/Post/index.html" , defaults=defaults)
        except Exception as e:
            self.set_status(500)
            self.render("errors/500.html")


class DoHelpHandler(AuthNeedBaseHandler):
   
    r"""
        @url:/dohelp/([0-9a-zA-Z]+)/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self, helpid):
        now_tm = time.time()
        try:
            data = yield self.application.db['permanent_help'].find_one({"helpid":helpid})
            if not data:
                self.set_status(404)
                self.render("errors/404.html")
                return 
            del data['_id']
            if 'expiretime' in data and data['expiretime'] < now_tm:
                data['state'] =2
            data['url'] = "/dohelp/"+helpid+"/"
            self.render("Help/Do/index.html", data=data, re=re)
        except Exception as e:
            self.set_status(500)     
            self.render("errors/500.html")

    @web.authenticated
    @gen.coroutine
    def post(self, helpid):
        tm = time.time()
        do_usercontact = self.get_argument("do_usercontact")
        do_usercontact_means = self.get_argument("do_usercontact_means")
        try:
            data = yield self.application.db['permanent_help'].find_one({"helpid":helpid})
            if data.get('expiretime', tm+100) < tm or data['state'] ==2 :
                if data['state'] != 2:
                    data['state'] = 2
                    yield self.application.db['permanent_help'].save(data)
                    yield self.application.db['updates_help'].remove({"helpid": helpid})
                self.render("Help/Do/result.html", result_text="Ta已经不需要帮助了")
            elif data['state'] == 0:
                data['state'] = 1
                data['do_userid'] = self.current_user['userid']
                data['do_username'] = self.current_user['username']
                data['do_userheadimgurl'] = self.current_user['headimgurl']
                data['do_usercontact'] = do_usercontact
                data['do_usercontact_means'] = str(do_usercontact_means)
                data['finishtime'] = time.time()
                resp = yield self.application.db['permanent_help'].save(data)
                yield self.application.db['updates_help'].remove({"helpid":helpid})
                criteria = {"userid":self.current_user["userid"]}
                modifier = {"$inc":{"help_cnt.done_help_num":1}};
                yield self.application.db['user'].update(criteria, modifier, upsert=True);
                # send help solved msg to post username
                self.application.task.send_task('worker.send_help_solved_msg', args=(
                                                             data['post_userid'],
                                                             data['do_username'],
                                                             data['do_usercontact'],
                                                             data['do_usercontact_means'],
                                                             data['post_username'],
                                                             data['posttime']
                                                ))
                self.redirect('/user/donehelp/') 
            else:
                self.render("Help/Do/result.html", result_text="已经有人帮助Ta了")
        except Exception as e:
            print(e)
            self.set_status(500)
            self.render("errors/500.html")


