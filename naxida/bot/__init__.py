r"""This package contains all the contents of naxida
"""
from typing import overload

from ._bot_main import *
from .charming import *
from .config import *
from .insert import *
from .manual import *
from .plugin import *
from .receive import *
from .send import *

__all__ = (
    "run",
    "insert_plugin", "insert_plugins", "get_plugin_info",
    "compat_msg", "grace",
    "schedule", "Rev", "Ciallo", "ciallo",
    "Insert",
    "InsertMessage",
    "InsertIni", "InsertSuper", "InsertPrivate",
    "InsertGroup", "InsertNotice", "InsertRequest",
    "IstMsg",
    "IstIni", "IstSuper", "IstPrivate",
    "IstGroup", "IstNotice", "IstRequest",
    "Manual", "Receive", "Send", "Config",
)

@overload
def run():...
@overload
def run(_prun:str, /):...
@overload
def run(*, _ciallo:str):...
@overload
def run(_prun:str, _ciallo:str, /):...
@overload
def run(_prun = None, _ciallo = None):...

def run(_prun = None, _ciallo = None):
    """Launch Portal"""
    if _prun: print(_prun)
    else: print('~~~少女祈祷中~~~')
    return bot_main(_ciallo)


def insert_plugin(module_name:str, search_path = None):
    """Import the plugins under search_path or path_plugins
    * If `search_path` is `None`, search `cwd` first,
      then search `path_plugins`

    Args:
    ```
        module_name:str   :Plugin Name
        search_path:str | None   :Find the path to the plugin
    ```

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

    Usages:
    ~~~~~~~
    ```
        import naxida

        for 'pkg' module in './plugins' dir:
            naxida.insert_plugin("pkg", "plugins")
            naxida.insert_plugin("pkg", "./plugins")
            naxida.insert_plugin("pkg", "./plugins/")

        for 'pkg' module in './' or './src/plugins' dir:
            naxida.insert_plugin("pkg")
    ```
    """
    plugin = Plugin([module_name],search_path)
    return plugin.insert_plugin(module_name)


def insert_plugins(dir_path:str):
    """Import multiple plugins in a folder
    * It will not import the ones starting with `_`

    Args:
    ```
        dir_path:str   :Relative paths to folders
    ```

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

    Usages:
    ~~~~~~~
    ```
        import naxida

        for 'plugins' dir in './' dir:
            naxida.insert_plugins("plugins")
            naxida.insert_plugins("./plugins")
            naxida.insert_plugin(".plugins")
            naxida.insert_plugins("./plugins/")

    ```
    """
    plugin = Plugin(search_path=dir_path)
    return plugin.insert_plugins(dir_path)


def get_plugin_info() -> str:
    """View all imported plugins"""
    return Plugin.get_info()


