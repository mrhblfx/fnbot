r"""This module is for quick import

For the convenience of use,this module imports some content from sub-modules,
the following content can be imported directly through this module

- `run` => `run` `<fnbot.bot.__init__>`
- `insert_plugin` => `insert_plugin` `<fnbot.bot.__init__>`
- `insert_plugins` => `insert_plugins` `<fnbot.bot.__init__>`
- `get_plugin_info` => `get_plugin_info` `<fnbot.bot.__init__>`
- `schedule` => `schedule` `<fnbot.bot.charming>`
- `Rev` => `Rev` `<fnbot.bot.charming>`
- `ciallo` => `cialo` `<fnbot.bot.charming>`
- `Insert` => `Insert` `<fnbot.bot.insert>`
- `InsertMessage` => `InsertMessage` `<fnbot.bot.insert>`
- `InsertIni` => `InsertIni` `<fnbot.bot.insert>`
- `InsertSuper` => `InsertSuper` `<fnbot.bot.insert>`
- `InsertPrivate` => `InsertPrivate` `<fnbot.bot.insert>`
- `InsertGroup` => `InsertGroup` `<fnbot.bot.insert>`
- `InsertNotice` => `InsertNotice` `<fnbot.bot.insert>`
- `InsertRequest` => `InsertRequest` `<fnbot.bot.insert>`
- `IstMsg` => `IstMsg` `<fnbot.bot.insert>`
- `IstIni` => `IstIni` `<fnbot.bot.insert>`
- `IstSuper` => `IstSuper` `<fnbot.bot.insert>`
- `IstPrivate` => `IstPrivate` `<fnbot.bot.insert>`
- `IstGroup` => `IstGroup` `<fnbot.bot.insert>`
- `IstNotice` => `IstNotice` `<fnbot.bot.insert>`
- `IstRequest` => `IstRequest` `<fnbot.bot.insert>`
- `Manual` => `Manual` `<fnbot.bot.manual>`
- `Receive` => `Receive` `<fnbot.bot.receive>`
- `Send` => `Send` `<fnbot.bot.send>`
- `Config` => `Config` `<fnbot.bot.config>`

---

Introduction:
~~~~~~~~~~~~~
This package is a python program that interfaces with go-cqhttp and
is primarily used on Linux (mostly on termux) and Windows platforms.
A simple, elegant, stable, batch, replicated qqbot can be created
in a convenient way.

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

Usages:
~~~~~~

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
"""

from .bot import run as run
from .bot import insert_plugin as insert_plugin
from .bot import insert_plugins as insert_plugins
from .bot import get_plugin_info as get_plugin_info

from .bot import schedule as schedule
from .bot import Rev as Rev
from .bot import Ciallo as Ciallo
from .bot import ciallo as ciallo

from .bot import Insert as Insert
from .bot import InsertMessage as InsertMessage
from .bot import InsertIni as InsertIni
from .bot import InsertSuper as InsertSuper
from .bot import InsertPrivate as InsertPrivate
from .bot import InsertGroup as InsertGroup
from .bot import InsertNotice as InsertNotice
from .bot import InsertRequest as InsertRequest
from .bot import IstMsg as IstMsg
from .bot import IstIni as IstIni
from .bot import IstSuper as IstSuper
from .bot import IstPrivate as IstPrivate
from .bot import IstGroup as IstGroup
from .bot import IstNotice as IstNotice
from .bot import IstRequest as IstRequest

from .bot import Manual as Manual
from .bot import Receive as Receive
from .bot import Send as Send
from .bot import Config as Config

from .__version__ import (
    __title__,
    __version__,
    __description__,
    __url__,
    __author__,
    __author_email__,
)


