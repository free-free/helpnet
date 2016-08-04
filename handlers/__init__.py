# coding=utf8
# Nothing is here

from tornado import gen,web
from tornado import ioloop
from tornado.httpclient import AsyncHTTPClient,HTTPRequest
from urllib.parse import urlencode
import json
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
    try:
        response = yield httpclient.fetch(req)
    except Exception:
        return None
    return response 
    

if __name__ == '__main__':
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

