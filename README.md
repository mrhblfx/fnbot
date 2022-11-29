# ともたけ よしの bot
*******************
_🌱 This project is based on the [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) and [fnbot](https://github.com/mrhblfx/fnbot) development of QQ entertainment robot 🌱_


## Quick Start(for windows)
+ Download the latest version of [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
+ Configure 'config.yml' generated by go-cqhttp

<details>
<summary>Example of config.yml</summary>
  
```yml
account: # 账号相关
  uin: 123456789 # QQ账号
  password: '' # 密码为空时使用扫码登录
```
and
```yml
# 连接服务列表
servers:
  # 添加方式，同一连接方式可添加多个，具体配置说明请查看文档
  #- http: # http 通信
  #- ws:   # 正向 Websocket
  #- ws-reverse: # 反向 Websocket
  #- pprof: #性能分析服务器

  - http: # HTTP 通信设置
      address: 127.0.0.1:9900 # HTTP监听地址
      timeout: 5      # 反向 HTTP 超时时间, 单位秒，<5 时将被忽略
      long-polling:   # 长轮询拓展
        enabled: false       # 是否开启
        max-queue-size: 2000 # 消息队列大小，0 表示不限制队列大小，谨慎使用
      middlewares:
        <<: *default # 引用默认中间件
      post:           # 反向HTTP POST地址列表
      #- url: ''                # 地址
      #  secret: ''             # 密钥
      #  max-retries: 3         # 最大重试，0 时禁用
      #  retries-interval: 1500 # 重试时间，单位毫秒，0 时立即
        - url: http://127.0.0.1:9901/ # 地址
          secret: ''                  # 密钥
          max-retries: 10             # 最大重试，0 时禁用
          retries-interval: 1000      # 重试时间，单位毫秒，0 时立即
```

</details>

+ Install python >= 3.8.10
+ Run `git clone https://github.com/mrhblfx/fnbot` on the command line
+ Configure `pybot.toml`

<details>
<summary>Example of pybot.toml</summary>
  
```toml
host = "127.0.0.1"
port = 9900
post = 9901
bot_qq = 123456789 # QQ account
group_list = [123456,1234567] # The group chat where QQbot is located
```

</details>

+ Run `python bot.py` on the command line
+ If the file `funcfg.json` is generated automatically, you don't need to care about it

> ***It's very simple for Linux, so I won't go into too much detail here***


## Plugin
- A plugin is a python module or package that can be anywhere
- fnbot imports plugins from `./src/plugins` and `./` by default, but this is not mandatory
- You can create a folder plugins in `./` and import plugins from the folder (by using `fnbot.insert_plugins("./plugins")`)

<details>
<summary>Example of a simple plugin</summary>

### Example of a simple plugin
In the `./src/plugins` folder, you can see the `test.py` file, which contains the following code:
```python
from fnbot import Rev
from fnbot import Send
from fnbot import IstMsg

@IstMsg.manage()
@Rev.grace()
async def _(msg_type:str, num_type:str, rev:'Rev'):
    if rev.match(['ciallo',]):
        msg = 'ciallo!'
        Send(rev).send_msg(msg_type, num_type, msg)
```
What the above code does is when you send `ciallo` in a group chat or private chat, your bot will send `ciallo!`

</details>

<details>
<summary>Example of a timed task</summary>

### Example of a timed task
In the `./plugins` folder, you can see the `basic.py` file, which contains the following code:
```python
import asyncio

from fnbot import IstNotice
from fnbot import schedule
from fnbot import ciallo
from fnbot import Send

@IstNotice.manage()
@ciallo.grace()
async def _(msg_type:str, num_type:str, rev:'ciallo'):
    if rev.notice_type == "group_recall":
        if rev.operator_id != rev.self_id:
            recall_rev = Send(rev).get_msg(rev.msg_id)['data']
            recall_rev = ciallo(recall_rev)
            recall_msg = recall_rev.msg

            msg = f"[CQ:poke,qq={recall_rev.sender_user_id}]"
            Send(rev).send_msg(msg_type,num_type,msg)

            msg = recall_msg
            msg_id = Send(rev).send_msg(msg_type,num_type,msg)

            @schedule
            async def task():
                await asyncio.sleep(1)
                Send(rev).delete_msg(msg_id)
                await task.cancel()
            await task.start(rev)
```
The above code implements that when someone withdraws a message in the group, the bot automatically sends the message that the person withdraws, and then withdraws the message it sent after one second

</details>

<details>
<summary>Example of complex scheduling task</summary>

### Example of complex scheduling task
In the `./plugins` folder, you can see the `test.py` file, which contains the following code:
```python
import time
import asyncio

from fnbot import IstMsg
from fnbot import ciallo
from fnbot import Send
from fnbot import schedule

@IstMsg.manage()
@ciallo.grace()
async def _(msg_type:str, num_type:str, rev:ciallo):
    if rev.match(["riddle",]):
        issue = (
            'Is it reasonable to '
            'treat the Me3Si group as if it were a big proton '
            'in some circumstances?'
        )
        answer = ['Yes', 'yes']
        now_time = time.strftime("%Y-%m-%d %H:%M:%S")
        msg = (
            f"[CQ:reply,id={rev.msg_id}]"
            f"[CQ:at,qq={str(rev.qq)}]"
            f"[CQ:at,qq={str(rev.qq)}]\n\n"
            f"{issue}\n\n"
            f"{now_time}"
        )
        msg = ciallo.compat_msg(msg, msg_type, rev)
        Send(rev).send_msg(msg_type, num_type, msg)

        frequency:int = 0
        @schedule
        async def task():
            nonlocal frequency
            while True:
                frequency += 1
                _rev = await rev.awtrev()
                if all((
                    _rev.msg == 'answer', _rev.identify_privilege(True),
                )):
                    msg = (
                        f"The answer is as follows:\n\n"
                        f"Yes or yes"
                    )
                    Send(rev).send_msg(msg_type, num_type, msg)
                    frequency -= 1
                elif _rev.msg in answer:
                    msg=(
                        f"[CQ:at,qq={rev.qq}]\n"
                        f"Congratulation on your correct answer!"
                    )
                    msg = ciallo.compat_msg(msg, msg_type, rev)
                    Send(rev).send_msg(msg_type, num_type, msg)
                    await task.cancel()
                elif frequency == 3:
                    msg = (
                        f"[CQ:at,qq={str(rev.qq)}]\n"
                        f"The maximum number of answers has been reached!\n"
                        f"The answer is as follows:\n\n"
                        f"Yes or yes"
                    )
                    msg = ciallo.compat_msg(msg, msg_type, rev)
                    Send(rev).send_msg(msg_type, num_type, msg)
                    await task.cancel()
                else:
                    msg=(
                        f"[CQ:at,qq={str(rev.qq)}]\n"
                        f"The answer doesn't seem to be this!"
                    )
                    msg = ciallo.compat_msg(msg, msg_type, rev)
                    Send(rev).send_msg(msg_type, num_type, msg)

        @task.awtwait
        async def task():
            while True:
                _rev = await rev.awtexcrev()
                if all((
                    _rev.msg == 'answer', _rev.identify_privilege(True),
                )):
                    msg = (
                        f"The answer is as follows:\n\n"
                        f"Yes or yes"
                    )
                    Send(rev).send_msg(msg_type, num_type, msg)

        @task.awtdecline
        async def task():
            await asyncio.sleep(180)
            msg = (
                f"[CQ:at,qq={rev.qq}]\n"
                f"Wait timeout!!!\n"
                f"The answer is as follows:\n\n"
                f"Yes or yes"
            )
            msg = ciallo.compat_msg(msg, msg_type, rev)
            Send(rev).send_msg(msg_type, num_type, msg)
            await task.cancel()
        await task.start(rev)
```
The above code achieves the following functions:
- When you send `riddle`, if you answer `Yes or yes` (when the number of times sent is less than or equal to three), the bot will send `Congratulation on your correct answer!`
- If you send something else but the number of times you send it is less than three, the bot will send `The answer doesn't seem to be this!`
- If you don't send anything, the bot will send `Wait timeout!!!    The answer is as follows:    Yes or yes`
- If you are `super_qq` or group owner or administrator, after sending `answer`, the bot will send `The answer is as follows: Yes or yes`

</details>


## unfinished to be continued


## ......


