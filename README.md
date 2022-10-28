# naxida_bot
Simple, elegant QQ bot processing package

You must install python3 beforehand

Then:
```
pip install naxida
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

* in `./src/plugins/test.py`:

```
from naxida import InsertPrivate
from naxida import InsertGroup
from naxida import grace_rev
from naxida import Send

@InsertPrivate.handle()
@InsertGroup.handle()
def _(rev:dict):
    if rev['message'] == '你好':
        Send.send_msg(
            rev['message_type'],rev['group_id'],
            '你好'
        )
    elif rev['message'] == 'こんにちは':
        Send.send_msg(
            rev['message_type'],rev['group_id'],
            'こんにちは'
        )


@InsertPrivate.manage()
@InsertGroup.manage()
@grace_rev('/test',['ciallo'])
def _(msg_type:str, num_type:str, rev_msg:str, qq:str, rev:dict):
    if rev_msg in ['ciallo']:
        msg = 'ciallo!'
        Send.send_msg(msg_type,num_type,msg)
```

---

* in `./bot.py`:

```
import naxida

naxida.insert_plugin("test")

if __name__ == "__main__":
    naxida.run()
```

---

This code means that when you send `你好`,`こんにちは` or `ciallo`
in the group or private, the bot will automatically reply `你好`,`こんにちは` or `ciallo`.
If you want to implement the above, you must fill in the necessary
information in `pybot.toml`.
