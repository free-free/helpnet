### url description:

'>' 符号表示需要登录才能访问
类似 '/resource/xxxx/' 这样的url都表示API,需要前台用ajax进行请求


|    url                                    |     description                          |
|:-----------------------------------------:|:----------------------------------------:|
| /                                         | 根目录,helplist,>                        |
| /askhelp/                                 | 发布请求,>                               |
| /logout/                                  | 登出,>                                   |
| /wxcallback/                              | 微信公众号事件额消息推送回调url          |
| /login/                                   | 登录页面，                               |
| /wxsublogin/                              | 微信网页认证URL                          |
| /search/                                  | 搜索页面,暂定,>                          |
| /about/                                   | 关于url,>                                |
| /document/                                | 文档url,>                                |
| /agreement/                               | 用户协议url,>                            |
| /user/                                    | 用户主页url,>                            |
| /user/gethelp/                            | 用户的帮助list url, >                    |
| /user/posthelp/                           | 用户发送的请求list url, >                |
| /user/profile/                            | 用户资料url(http get),修改资料(http post),>|
| /resource/WXQRCodeResource/get/           | 公众号关注二维码 API url，返回二维码url,>|
| /resource/HelpContenResource/get/         | 获取某一地点周围的请求，需要带上经纬度,> |
| /help/([0-9a-z-A-Z]+)/                    | 某一请求的详情页url,>                    |

#### Note:
>  /resource/HelpContentResource/get/ 的请求参数

```python
   param ={
        'source_url':'发出请求的js所在页面url',
        'context' : '请求上下文,可选值 ["updates","upost","uget"],
        'qrc': "请求条件"
   }     
   当 'context' = "updates" 请求条件qrc={"lng":"经度","lat":"纬度","last_help_pt":"上次请求返回数据的posttime,等于0时表式返回最新的数据"}
   当 'context' = "upost"  ,qrc ={"last_help_pt":"同上"}
   当 'context' = "uget"  ,qrc ={"last_help_pt":"同上"}
```

> /resource/HelpContentResource/get/ 相应数据

```python
   response = {
	'res_qrc':响应的请求的条件,以便下一次请求使用，字段和qrc的相同,
        'data': 响应的数据(数组),每一个数据代表每一个help单子的数据(post_userheadimgurl,helpcontent,helpstate,helprewad,post_username,helpremark)
   }
```
### updating ......
