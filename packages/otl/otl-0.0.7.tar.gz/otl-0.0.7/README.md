# **otl 工具集**
---
# 安装方式
```shell script
pip install otl
```
---

### 封装企业微信接口
```python
from otl.wechat.wechat_api import WechatApi

GLOBAL_WECHAR_CONFIG = {
        'NAME': 'xxx',

        #企业的id，在管理端->"我的企业" 可以看到
        'CORP_ID': '',

        #应用列表 可以配置多个应用
        'APP_LIST': {
            'warning_robot': {           #报警机器人
                'APP_ID': '',           #APPID
                'APP_SECRET': '',       #APP密钥
                'switch': 'on',          #是否开启
            },
        }
    }

if __name__ == '__main__':
    we = WechatApi(GLOBAL_WECHAR_CONFIG)
    status, res = we.apps['warning_robot'].send(
        msg_type='text',
        to_users_list=['xxx'],
        msg_string='xxx'
    )
    if not status:
        print(res)
```
### 封装mysql方法
```python
from otl.db import MysqlDbBase


class Db1(MysqlDbBase):
    host = '1.1.1.1'
    port = 3306
    user = 'test_user'
    password = 'test_pwd'
    db = 'test_db'

# 实例化
db1 = Db1()
# 查询操作 -> 返回数据: list
db1.query("select ***")
# 写入操作 -> 返回影响行数: int
db1.insert("insert into ***")
# 更新操作 -> 返回影响行数: int
db1.update("update ***")
# 删除操作 -> 返回影响行数: int
db1.delete("delete ***")
```