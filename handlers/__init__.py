# coding=utf8

import json
import time
import base64
import hmac
import timeit
from urllib.parse import urlencode, parse_qsl

from tornado import gen,web
from tornado import ioloop
from tornado.httpclient import AsyncHTTPClient,HTTPRequest


@gen.coroutine
def send_async_request(url, method="GET", headers={},body=""):
    if method.upper() == "POST":
        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body,dict):
        body = urlencode(body)
    req = HTTPRequest(url,
                     method=method,
                     headers=headers,
                     body=body,
                     allow_nonstandard_methods=True
                     )
    httpclient = AsyncHTTPClient()
    response = yield httpclient.fetch(req)
    return response 


def generate_state(key, state_expire=3600, **kwargs):
    r'''
        @Args:
            key: str
            state_expire: int
        @Return:
            state: str
    '''
    if state_expire == 0:
        ts_str = "0"
    else:
        ts_str = str(time.time()+state_expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr  = hmac.new(key.encode("utf-8"),ts_byte,'sha1').hexdigest()
    qs_str = urlencode(kwargs)
    state = ts_str + ':' + sha1_tshexstr + ':' + qs_str
    b64_state = base64.urlsafe_b64encode(state.encode("utf-8"))
    return b64_state.decode("utf-8")

def certify_state(key, state):
    r'''
        @Args:
            key: str
            state: str
        @Returns:
            boolean
    '''
    try:
        state_str = base64.urlsafe_b64decode(state).decode('utf-8')
        state_list = state_str.split(':')
        if len(state_list) != 3:
            return False
        ts_str = state_list[0]
        if float(ts_str) != 0 and float(ts_str) < time.time() :
            # state expired
            return False
        known_sha1_tsstr = state_list[1]
        sha1 = hmac.new(key.encode("utf-8"),ts_str.encode('utf-8'),'sha1')
        calc_sha1_tsstr = sha1.hexdigest()
        if calc_sha1_tsstr != known_sha1_tsstr:
            # state certification failed
            return False
        return dict(parse_qsl(state_list[2])) or True
    except Exception: 
        return False 
    # state certification success
    return True 
     

if __name__ == '__main__':
    def test_state():
        state = generate_state("huzhugc.com",0, redirect="http://www.huzhugc.com/user/postedhelp/")
        auth_url = "https://open.weixin.qq.com/connect/oauth2/authorize?\
appid={0}&redirect_uri={1}&response_type=code&scope=snsapi_base&state={2}#wechat_redirect"
        auth_url = auth_url.format("wxdfd14622e7cf37bc","http://www.huzhugc.com/wxpublogin/",state)
        return auth_url

    print(timeit.timeit('test_state()','from __main__ import test_state',number=1))
    r'''
    token = "wsSLlSIeJR-y5ghocGjHQpfLp97raFyGizissm6Tn6HTrq8rjLNSMV_z49ggBanRF1qScppSLF_TEbaWQnQbkgfzI97TwVwHR3ojRUJikFt9ZJ8aVZ4lFsqiZEywY4hyTEEfAJAXII"
    ticket = "gQFG8ToAAAAAAAAAASxodHRwOi8vd2VpeGluLnFxLmNvbS9xL0h6cGEwNFhtd05TNUlYS0dXUlRQAAIE7RSjVwMEgDoJAA=="
    loop = ioloop.IOLoop.current()
    @gen.coroutine
    def request():
        url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token="+token
        body = {"expire_seconds": 604800, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": 123}}}
        body = json.dumps(body)
        response = yield send_async_request(url, method="POST", body=body)
        print(response.body.decode("utf-8"))
        print(response.reason)
        print(response.headers)
    @gen.coroutine
    def get_qrcode():
        url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket="+ticket
        print(url)
        response = yield send_async_request(url)
        print(response.body)
        print(response.reason)
        print(response.headers)         
    loop.run_sync(request)
    '''

