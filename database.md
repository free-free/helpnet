
## user table
| field name   |  description            |
|:------------:|:-----------------------:|
|subscribe     |                         |
|userid        |   weixin openid         |
|username      |  weixin nickname        |
|usercontact   |                         |
|sex           |                         |
|city          |                         |
|country       |                         |
|province      |                         |
|language      |                         |
|headimgurl    |                         |
|createtime    |                         |
|address       |                         |
|location:lng,lat|                       |
|locprec       |                         |
|help_cnt:posted_help_num,done_help_num| |

## help table
| field             |     description    |
|:-----------------:|:------------------:|
|helpid             |   unique help id   |
|post_username      |   user nickname    |
|post_userid        |   unique user id   |
|post_userheadimgurl|   user header img url|
|post_usercontact   |                    |
|post_usercontact_means| "1"=="phone" "2"=="weixin" "3"=="qq" |
|address            |                    |
|content            |   help main content|
|price              |  help tip          |
|do_userid          |  help user id      |
|do_username        |                    |
|do_userheadimgurl  |                    |
|do_usercontact     |                    |
|do_usercontact_means|  same as "post_usercontact_means" |
|posttime           |  post timestamp    |
|finishtime         |                    |
|expiretime         | when user set expire time,this field will exists|
|help_state         |                    |
|location:lng,lat   |  array             |




