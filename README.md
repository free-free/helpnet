### url description:

'>' 符号表示需要登录才能访问
类似 '/resource/xxxx/' 这样的url都表示API,需要前台用ajax进行请求


|    url                                    |     description                          |
|:-----------------------------------------:|:----------------------------------------:|
| /                                         | 根目录,helplist,>                        |
| /logout/                                  | 登出,>                                   |
| /wxcallback/                              | 微信公众号事件或消息推送回调url          |
| /login/                                   | 登录页面，                               |
| /wxpubloginredirect/                      | 微信公众登陆重定向url                    |
| /wxpublogin/                              | 微信网页认证URL                          |
| /feelback/                                | 用户反馈意见,>                           |
| /posthelp/                                 | 发布请求,>                               |
| /dohelp/([a-zA-Z0-9]+)/?                  | 接受的求助                               |
| /search/                                  | 搜索页面,暂定,>                          |
| /user/                                    | 用户主页url,>                            |
| /user/donehelp/                            | 用户的帮助list url, >                    |
| /user/postedhelp/                           | 用户发送的请求list url, >              |
| /resource/WXJSAPIResource/get/?           | 获取微信jsapi ticket,>                   | 
| /resource/WXQRCodeResource/get/           | 公众号关注二维码 API url，返回二维码url,>|
| /resource/UpdatesHelpResource/get/        | 获取某一地点周围的请求，需要带上经纬度,> |
| /resource/DoneHelpResource/get/           | 获取某一用户的帮助,>                     |
| /resource/PostedHelpResource/get/         | 获取某一用户的求助,>                     |
| /resource/HelpResource/delete/            | 删除某一求助,>                           |
| /resource/UserPositionResource/update/    | 更新用户位置                             |

### API 说明:

####  API: /resource/UpdatesHelpResource/get/ 

> 请求参数

```python
   request = {
        'source_url':'发出请求的js所在页面url',
        'data':{
            'context' :{"lng":"longitude", "lat":"latitude", "last_help_pt":"last help psottime timestamp"} 
            'qrc': {"rcd_num":"number"} //rcd_num==> records number 
        }
   }

   !!Note:
        1. when 'last_help_pt' equal to 0.0, that represents server will return latest help data
        2. when 'lng' and 'lat' is optional. 
```
> 响应数据

```python
   response = {
	'resp_qrc':{"last_help_pt": "**", "rcd_num":"record number ",
        'resp':[
              {'post_userheadimgurl': '**',
               'content': '**',
               'state': '**',
               'price': '**',
               'post_username': '**'
               'address': '**',
               'post_datetime': 'isoformat',
               'posttime':'**',
               'helpid': '**'
              },...
         ]
   }
```


####  API: /resource/PostedHelpResource/get/ 

> 请求参数

```python
   request = {
        'source_url':'发出请求的js所在页面url',
        'data':{
            'context': {"last_help_pt":"last help data posttime"},
            'qrc': {"rcd_num": ""}
        }
   }     
 
```
> 响应数据

```python
   response = {
	'resp_qrc': {"last_help_pt": "**", "rcd_num": "**"},
        'resp': [
            {
             'helpid': '',
             'post_userheadimgurl': '', 
             'post_username': '',
             'content': '', 
             'address': '',
             'post_usercontact': '', 
             'post_usecontact_means': '',
             'state': '', 
             'price': '',
             'posttime': '',
             'post_datetime': '%Y/%m/%d %H:%M:%S',
             'do_username':''
             'do_userheadimgurl': '',
             'do_usercontact': '',
             'do_usercontact_means':''
            },...
       ]
             
   }
```


####  API: /resource/DoneHelpResource/get/ 

> 请求参数

```python
   request = {
        'source_url':'发出请求的js所在页面url',
        'data':{
            'context' : {"last_help_pt":" last help data posttime"},
            'qrc': {"rcd_num": "record number"}
        }
   }     
```
> 响应数据

```python
   response = {
	'resp_qrc':{"rcd_num": "recorder number", "last_help_pt:"**"},
        'resp':[
               {'post_userheadimgurl': '',
                'post_username': '',
                'post_usercontact': '', 
                'content', ''
                'state': '', 
                'price': '',
                'address': '',
                'posttime': '',
                'post_datetime': '%Y/%m/%d %H:%M:%S'
                },...
         ]
   }
```


#### API:  /resource/WXQRCodeResource/get/

> 请求参数

```python
     request = {
            'source_url':'同上',
            'data':{
                'context' : ''，
                'qrc ' : ''
            }
     }
```

> 响应数据

``` python 
    response = {
          'resp_qrc': {},
          'resp':[{'qrcode_url':"url"},...]
    }
```

#### API: /resource/WSJSApiResource/get/

> 请求参数

```python

    request = {
              "source_url:"同上",
              "data":{
                  "context":"",
                  "qrc": ""
              }
    }
```

> 响应数据

```python
    response = {
        'resp_qrc':request.qrc,
        'resp':[{
            "appid":"",
            "noncestr":"",
            "signature":"",
            "api_list":["openLocation", "getLocation"],
            "timestamp":""
        }]
    }
```

#### API: /resource/UserPositionResource/update/

> request parameters

```python
    request = {
              "source_url":"same as before",
              "data":{
                   "lng":"",
                   "lat":"",
              }
    }
```

> response data

```python
    response = {
          "resp_qrc":"",
          "resp":{"result":"OK/NO", "code":0/-1}
    }

```

#### API: /resource/UserProfileResource/get/

> 请求参数

```python
    request = {
          'source_url':'/user/profile/',
          'data':{
              'context':'',
              'qrc':'',
          }
    }
```

> 响应数据

```python
   response = {
          'resp_qrc':'',
          'resp':[{'user_contact':'mobile phone number'}]
   }
```

#### API: /resource/UserProfileResource/update/

> 请求参数

```python
    request = {
          'source_url':'/user/profile',
          'data':{
              'context':{'user_contact':"用户修改的mobile phone number"},
              'qrc':''
          }
    }
```

> 响应数据

```python
    response = {
          'resp_qrc':'',
          'resp':[]
   }

```
### updating ......
