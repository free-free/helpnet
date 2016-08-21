# coding:utf-8

from tornado import web
import hashlib

TOKEN = "huzhugctoken"
class CheckSignatureHandler(web.RequestHandler):

    def get(self):
        signature = self.get_argument("signature","")
        timestamp = self.get_argument("timestamp","")
        nonce = self.get_argument("nonce","")
        echostr = self.get_argument("echostr","")
        param_list = [TOKEN,timestamp,nonce]
        param_list.sort()
        param_str = ''.join(param_list).encode()
        sha1 = hashlib.sha1()
        sha1.update(param_str)
        param_str = sha1.hexdigest()
        if signature == param_str:
            self.write(echostr)
        else:
            self.write("")
        

