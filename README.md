# telegrambackup
基于[tg-archive](https://github.com/knadh/tg-archive)实现telegram数据备份展示的增强项目

特性:
* 支持增量备份
* 支持同时维护与展示多个channel/group聊天数据



# 实战

1. git clone this repo

2. 安装依赖:

    ```bash
    py -3 -m pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
    ```

3. 初始化配置, 编辑config.py, 可参考如下:

    * telegram_name 为自己的备份项目取个名

    * groups

      > 如果是通过浏览器访问telegram，点击目标会话后，在URL处可以看到类似web.telegram.org/z/#-7XXX , 那么不带负号的 7XXX 即为id

      ```
      id: {
      	"name": "为group/channel取个名",
      	"sync": True, # 是否同步消息
      	"build": True # 是否展示聊天数据
      },
      ```

    * defaults

      ```
      "api_id": "",
      "api_hash": "",
      "proxy": {
      	"enable": True,
      	"protocol": "socks5",
      	"addr": "127.0.0.1",
      	"port": 1081
      },
      "publish_rss_feed": False
      ```

4. 执行程序 main.py

5. 首次执行/会话失效会要求输入注册telegram使用的密码, 例如 +1xxxxx ，则输入 1xxxx ，不带加号， 然后在telegram上获取验证码

6. 等待数据同步与站点构建完成

7. 访问18000端口即可查看聊天数据