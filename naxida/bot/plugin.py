import os
import json
import importlib

from .config import *
from .manual import *

__all__ = "Plugin",

class Plugin():
    """Store the plugin and its location information

    Class Properties:
    ```
        inserted_plugins:dict
    ```

    Instance Properties:
    ```
        plugin_list:list | None
        search_path:str | None
    ```
    """
    inserted_plugins:dict = {}
    """
    ```
    {
        module:'module' : path:str,
        ...
    }
    ```
    """
    def __init__(self, plugin_list = None, search_path = None):
        self.plugin_list = plugin_list
        self.search_path = search_path


    def _path_name(self, name:str = '', path:str = '') -> str:
        if path == None:
            return name
        elif path == self.search_path:
            i_name = Config.path_plugins.split(Config.path_pybot)[-1].lstrip("/")
            name =  ".".join(i_name.split("/")) + f".{name}"
            return name
        elif path == Config.path_plugins:
            i_name = Config.path_plugins.split(Config.path_pybot)[-1].lstrip("/")
            name =  ".".join(i_name.split("/")) + f".{name}"
            return name


    def insert_plugin(self, name:str):
        _plugin_search_list = os.listdir(self.search_path)
        """Default launcher path"""
        plugin_search_list = [
            i for i in _plugin_search_list if not i.startswith('_')
        ]

        if os.path.exists(Config.path_plugins):
            _plugin_src_list = os.listdir(Config.path_plugins)
            plugin_src_list = [
                i for i in _plugin_src_list if not i.startswith('_')
            ]
        else:
            plugin_src_list = []

        if any((
            name in plugin_search_list,
            name + '.py' in plugin_search_list,
        )):
            module = importlib.import_module(
                self._path_name(name, self.search_path)
            )
            if name + '.py' in plugin_search_list:
                name = name + '.py'

            if self.search_path != None:
                self.inserted_plugins.update(
                    {
                        str(module):self.search_path + f"/{name}"
                    }
                )
            else:
                self.inserted_plugins.update(
                    {
                        str(module):Config.path_pybot + f"/{name}"
                    }
                )
        elif any((
            name in plugin_src_list,
            name + '.py' in plugin_src_list,
        )):
            module = importlib.import_module(
                self._path_name(name, Config.path_plugins)
            )
            if name + '.py' in plugin_src_list:
                name = name + '.py'

            self.inserted_plugins.update(
                {
                    str(module):Config.path_plugins + f"/{name}"
                }
            )
        else:
            raise RuntimeError(f"Not found {name}!!!")


    def insert_plugins(self, dir_path:str):
        dir_path = dir_path.replace(".","")
        dir_path_abs = Config.path_pybot + "/" + dir_path
        dir_list = os.listdir(dir_path_abs)
        dir_list = [i for i in dir_list if not i.startswith('_')]
        if dir_list == []:
            raise RuntimeError("Not found any plugin!!!")
        for i in dir_list:
            name = dir_path + f".{i.rstrip('.py')}"
            module = importlib.import_module(name)
            self.inserted_plugins.update(
                {
                    str(module):dir_path_abs + "/" + i
                }
            )


    @classmethod
    def look_inserted_plugins(cls):
        _plugins = json.dumps(
            cls.inserted_plugins, sort_keys=True,
            indent=4, separators=(',', ':'),
            ensure_ascii=False,
        )
        return _plugins
