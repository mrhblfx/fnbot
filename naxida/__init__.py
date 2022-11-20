r"""This module is for quick import

For the convenience of use,this module imports some content from sub-modules,
the following content can be imported directly through this module

- `run` => `run` `<naxida.bot.__init__>`
- `insert_plugin` => `insert_plugin` `<naxida.bot.__init__>`
- `insert_plugins` => `insert_plugins` `<naxida.bot.__init__>`
- `get_plugin_info` => `get_plugin_info` `<naxida.bot.__init__>`
- `compat_msg` => `compat_msg` `<naxida.bot.charming>`
- `grace` => `grace` `<naxida.bot.charming>`
- `schedule` => `schedule` `<naxida.bot.charming>`
- `Rev` => `Rev` `<naxida.bot.charming>`
- `ciallo` => `cialo` `<naxida.bot.charming>`
- `Insert` => `Insert` `<naxida.bot.insert>`
- `InsertMessage` => `InsertMessage` `<naxida.bot.insert>`
- `InsertIni` => `InsertIni` `<naxida.bot.insert>`
- `InsertSuper` => `InsertSuper` `<naxida.bot.insert>`
- `InsertPrivate` => `InsertPrivate` `<naxida.bot.insert>`
- `InsertGroup` => `InsertGroup` `<naxida.bot.insert>`
- `InsertNotice` => `InsertNotice` `<naxida.bot.insert>`
- `InsertRequest` => `InsertRequest` `<naxida.bot.insert>`
- `IstMsg` => `IstMsg` `<naxida.bot.insert>`
- `IstIni` => `IstIni` `<naxida.bot.insert>`
- `IstSuper` => `IstSuper` `<naxida.bot.insert>`
- `IstPrivate` => `IstPrivate` `<naxida.bot.insert>`
- `IstGroup` => `IstGroup` `<naxida.bot.insert>`
- `IstNotice` => `IstNotice` `<naxida.bot.insert>`
- `IstRequest` => `IstRequest` `<naxida.bot.insert>`
- `Manual` => `Manual` `<naxida.bot.manual>`
- `Receive` => `Receive` `<naxida.bot.receive>`
- `Send` => `Send` `<naxida.bot.send>`
- `Config` => `Config` `<naxida.bot.config>`

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
from naxida import Send
from naxida import Rev
from naxida import IstMsg

@IstMsg.manage()
@Rev.grace('/test')
async def _(msg_type:str, num_type:str, rev:'Rev'):
    if rev.match(['ciallo', 'こんにちは', '你好']):
        msg = 'ciallo!'
        Send.send_msg(msg_type,num_type,msg)
```

---

* for `./bot.py`:

```
import naxida

naxida.insert_plugin("test")

if __name__ == "__main__":
    naxida.run()
```

... or
```
>>> import naxida
>>> naxida.insert_plugin("test")
>>> naxida.run()
```
"""

from .bot import run as run
from .bot import insert_plugin as insert_plugin
from .bot import insert_plugins as insert_plugins
from .bot import get_plugin_info as get_plugin_info

from .bot import compat_msg as compat_msg
from .bot import grace as grace
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


