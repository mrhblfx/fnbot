r"""This module is for quick import

For the convenience of use,this module imports some content from sub-modules,
the following content can be imported directly through this module

- `run` => `run` `<naxida.bot.__init__>`
- `compat_msg` => `compat_msg` `<naxida.bot.__init__>`
- `grace_rev` => `grace_rev` `<naxida.bot.__init__>`
- `grace` => `grace` `<naxida.bot.__init__>`
- `logerr` => `logerr` `<naxida.bot._bot_main>`
- `insert_plugin` => `insert_plugin` `<naxida.bot.__init__>`
- `insert_plugins` => `insert_plugins` `<naxida.bot.__init__>`
- `lool_inserted_plugins` => `lool_inserted_plugins` `<naxida.bot.__init__>`
- `Manual` => `Manual` `<naxida.bot.manual>`
- `Receive` => `Receive` `<naxida.bot.receive>`
- `Send` => `Send` `<naxida.bot.send>`
- `Config` => `Config` `<naxida.bot.config>`
- `InsertIni` => `InsertIni` `<naxida.bot.insert>`
- `InsertOthers` => `InsertOthers` `<naxida.bot.insert>`
- `InsertSuper` => `InsertSuper` `<naxida.bot.insert>`
- `InsertPrivate` => `InsertPrivate` `<naxida.bot.insert>`
- `InsertGroup` => `InsertGroup` `<naxida.bot.insert>`
- `InsertNotice` => `InsertNotice` `<naxida.bot.insert>`
- `InsertRequest` => `InsertRequest` `<naxida.bot.insert>`
- `IstIni` => `IstIni` `<naxida.bot.insert>`
- `IstOthers` => `IstOthers` `<naxida.bot.insert>`
- `IstSuper` => `IstSuper` `<naxida.bot.insert>`
- `IstPrivate` => `IstPrivate` `<naxida.bot.insert>`
- `IstGroup` => `IstGroup` `<naxida.bot.insert>`
- `IstNotice` => `IstNotice` `<naxida.bot.insert>`
- `IstRequest` => `IstRequest` `<naxida.bot.insert>`

---

Introduction:
~~~~~~~~~~~~~
This package is a self-developed python program for Linux(termux) and Windows,
docked to go-cqhttp for processing via http communication,
mainly for learning and self-use.

The default file tree:
~~~~~~~~~~~~~~~~~~~~~~
```
.
├── bot.py
├── pybot.toml
├── src
│   ├── plugins
|   |    ├── ...
|   |    ├── ...
```

Cautions:
~~~~~~~~~
* The file `pybot.yoml` needs to be created by you,
  with the following format:

```
[`Write whatever you like`]
host = # It must exist
port = # It must exist
post = # It must exist
bot_qq = # It must exist
group_list = # It must exist
nickname = # This is optional
super_qq = # This is optional
admin_list = # This is optional
blackqq_list = # This is optional
```

* If you don't like to create the file `pybot.yoml`,
  then the default configuration is as follows:

```
{
    'host': '127.0.0.1',
    'port': 9900,
    'post': 9901,
    'bot_qq': 0,
    'group_list': [],
    'nickname': '',
    'super_qq': 0,
    'admin_list':[],
    'blackqq_list':[],
}
```

* And you need to create your own `./src/plugins` folder
  (This is not a necessary step)
* Plugins can be located in the current directory,
  under the folder `./src/plugins`, and in custom locations.
  However, it is usually better to locate it under the folder `./src/plugins`

---

Usage:
~~~~~~

---

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

"""

from .bot import run as run
from .bot import compat_msg as compat_msg
from .bot import grace as grace
from .bot import grace_rev as grace_rev
from .bot import logerr as logerr
from .bot import insert_plugin as insert_plugin
from .bot import insert_plugins as insert_plugins
from .bot import look_inserted_plugins as look_inserted_plugins

from .bot import Manual as Manual
from .bot import Receive as Receive
from .bot import Send as Send
from .bot import Config as Config
from .bot import IstIni as IstIni
from .bot import IstOthers as IstOthers
from .bot import IstSuper as IstSuper
from .bot import IstPrivate as IstPrivate
from .bot import IstGroup as IstGroup
from .bot import IstNotice as IstNotice
from .bot import IstRequest as IstRequest
from .bot import InsertIni as InsertIni
from .bot import InsertOthers as InsertOthers
from .bot import InsertSuper as InsertSuper
from .bot import InsertPrivate as InsertPrivate
from .bot import InsertGroup as InsertGroup
from .bot import InsertNotice as InsertNotice
from .bot import InsertRequest as InsertRequest

from .__version__ import (
    __title__,
    __version__,
    __description__,
    __url__,
    __author__,
    __author_email__,
)


