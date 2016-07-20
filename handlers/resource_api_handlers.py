#-*- coding:utf-8 -*-

from tornado import web
from tornado import ioloop
from tornado import gen
from tornado import template
from .base_handler import BaseHandler, AuthNeedBaseHandler


class ResourceBaseHandler(AuthNeedBaseHandler):

    @gen.coroutine
    def prepare(self):
        if self.request.headers.get("X-Requested-With") != "XMLHttpRequest":
            self.write("some thing wrong")
            self.finish()
        else:
            yield super(ResourceBaseHandler, self).prepare()

############################################################
#
#
#@ user settings resource handler
#
#
#
##########################################################


class ResourceUserSettingsResourceUpdateHandler(ResourceBaseHandler):

    r"""
        @url:/resource/UserSettingsResource/update
    """
    @web.authenticated
    @gen.coroutine
    def post(self):
        pass


class ResourceUserSettingsResourceGetHandler(ResourceBaseHandler):
    r"""
        @url:/resource/UserSettingsResource/get
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        self.write("user settings resource")


##################################################################
#
#
#@url user profile handler
#
#
###############################################################
class ResourceUserProfileContextResourceGetHandler(ResourceBaseHandler):
    r"""
        @url:/resource/UserProfileContextResource/get/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        pass


class ResourceUserProfileResourceGetHandler(ResourceBaseHandler):
    r"""
        @url:/resource/UserProfileResource/get/?
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        pass


class ResourceUserProfileResourceUpdateHandler(ResourceBaseHandler):
    r"""
        @url:/resource/UserProfileResource/update/?
    """
    @web.authenticated
    @gen.coroutine
    def post(self):
        pass
