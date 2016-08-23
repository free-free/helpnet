# coding=utf-8

import json
import requests
from redis import Redis

def create_menu():
    redis =  Redis("localhost", 6379)
    access_token = redis.get("weixin_api_token")
    access_token = access_token.decode()
    url =  "https://api.weixin.qq.com/cgi-bin/menu/create?access_token={0}"
    url = url.format(access_token)
    data = {
        "button":[
             {
                 "type": "view",
                 "name": "寻求帮助",
                 "url": "http://www.huzhugc.com/wxpubloginredirect/"
             },
         ]
    }
    req = requests.post(url, data=data)
    return req.json()


if __name__ == '__main__':
    print(create_menu())
   

