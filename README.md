# fnbot
Simple, elegant QQ bot processing package

You must install python3 beforehand

Then:
```
pip install fnbot
```
... or
```
pip install -r requirements.txt
```

## Configuration
The configuration information is in **pybot.toml**

The example configuration is as follows:

```toml
host = "127.0.0.1"
port = 9900
post = 9901
bot_qq = 123456789 # The QQ number of the QQ bot you want to set up.
group_list = [123456,1234567] # The qq group number that can use QQ bot function.
```

## The default file tree:

```
.
├── bot.py
├── pybot.toml
├── src
│   ├── plugins
|   |    ├── ...
|   |    ├── ...
```


## Usage:

* for `./src/plugins/test.py`:

```
from fnbot import Send
from fnbot import Rev
from fnbot import IstMsg

@IstMsg.manage()
@Rev.grace('/test')
async def _(msg_type:str, num_type:str, rev:'Rev'):
    if rev.match(['ciallo', 'こんにちは', '你好']):
        msg = 'ciallo!'
        Send(rev).send_msg(msg_type,num_type,msg)
```

---

* for `./bot.py`:

```
import fnbot

fnbot.insert_plugin("test")

if __name__ == "__main__":
    fnbot.run()
```

... or
```
>>> import fnbot
>>> fnbot.insert_plugin("test")
>>> fnbot.run()
```

---

This code means that when you send `你好`,`こんにちは` or `ciallo`
in the group or private, the bot will automatically reply `ciallo!`.
If you want to implement the above, you must fill in the necessary
information in `pybot.toml`.
