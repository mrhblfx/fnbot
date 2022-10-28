r"""This package contains all the contents of naxida

The reason for creating the package `naxida` is for the convenience of
use. As more and more features are added to the bot, the disadvantage
that it becomes harder to manage quickly becomes apparent,especially
when the bot's code is updated from another device (like a cell phone).
So there is this `naxida` package, which currently runs 'stable' on
both windows and linux systems (including `termux` on cell phones).
"""

from ._bot_main import *
from .insert import *
from .manual import *
from .plugin import *
from .send import *
from .receive import *
from .config import *

from .internal_plugins import *

__all__ = (
    "run", "compat_msg", "grace_rev", "grace", "logerr",
    "insert_plugin", "insert_plugins", "look_inserted_plugins",
    "InsertIni", "InsertOthers", "InsertSuper",
    "InsertPrivate", "InsertGroup", "InsertNotice", "InsertRequest",
    "IstIni", "IstOthers", "IstSuper",
    "IstPrivate", "IstGroup", "IstNotice", "IstRequest",
    "Manual","Receive", "Send", "Config",
)

def run():
    """run bot"""
    print("~~~少女祈祷中~~~")
    return bot_main()


def insert_plugin(module_name:str, search_path = None):
    """Import the plugins under search_path or path_plugins
    * If `search_path` is `None`, search `cwd` first,
      then search `path_plugins`

    Args:
    ```
        module_name:str :Plugin Name
        search_path:str | None :Find the path to the plugin
    ```
    """
    plugin = Plugin([module_name],search_path)
    return plugin.insert_plugin(module_name)


def insert_plugins(dir_path:str):
    """Import multiple plugins in a folder

    Args:
    ```
        dir_path:str :Relative paths to folders
    ```
    """
    plugin = Plugin(search_path=dir_path)
    return plugin.insert_plugins(dir_path)


def look_inserted_plugins() -> dict:
    """View all imported plugins"""
    return Plugin.look_inserted_plugins()


def compat_msg(msg:str, msg_type:str, rev:dict) -> str:
    """Make the messages to be sent compatible with
    group chats and private chats

    Args:
    ```
        msg:str
        msg_type:str
        rev:dict
    ```

    Returns:
    ```
        msg:str
    ```

    Raises:
    ```
        TypeError
    ```
    """
    if msg_type == "private":
        if msg.startswith("[CQ:at,qq="):
            msg = msg.split("]",1)[-1]
            msg = msg.lstrip("\n")
            msg = "@" + rev['sender']['nickname'] + "\n" + msg
            return msg
        elif msg.startswith("[CQ:reply,id="):
            _, __, msg = msg.split("]",2)
            msg = msg.split("]",1)[-1]
            msg = "@" + rev['sender']['nickname'] + msg
            msg = _ + "]" + __ + "]" + msg
            return msg
    elif msg_type == "group":
        return msg
    else:
        raise TypeError("Be careful!")


def grace_rev(_nickname = None, _cmd = None):
    """Elegant

    * Decorate a function to make it look simpler
    * Usually used when `InsertPrivate` and `InsertGroup` are available

    Args:
    ```
        _nickname:str | None : Customized function names
        _cmd:list : The command triggered by the function you added
    ```

    Returns:
    ```
        msg_decorator:'function'
        msg_decorator(f:'function') -> decorator:'function'
        decorator(rev:dict) -> f(msg_type, num_type, rev_msg, qq, rev)
    ```

    Raises:
    ```
        TypeError
    ```

    ---

    Examples are as follows:
    ~~~~~~~~~~~~~~~~~~~~~~~~
    ```
    @InsertGroup.manage()
    @grace_rev()
    def _(msg_type:str, num_type:str, rev_msg:str, qq:str, rev:dict):
        # msg = 'ciallo'
        # Send(rev).send_msg(msg_type,num_type,msg)
        ...
    ```

    `Hint:The above five parameters are mandatory`

    In terms of results, this is equivalent to the following example,
    but the above is more concise
    ```
    @InsertGroup.manage()
    def _(rev:dict):
        msg_type = 'group' if 'group_id' in rev else 'private'
        qq:str = str(rev['user_id']) if 'user_id' in rev else ''
        group_id:str = str(rev['group_id']) if 'group_id' in rev else ''
        num_type:str = qq if msg_type == 'private' else group_id
        rev_msg:str = rev['message'] if 'message' in rev else ''
        ...
    ```
    ---
    The purpose of this decorator is to adapt to the ancient version
    of the plug-in and simplify the code
    """
    def msg_decorator(f:'function'):
        def decorator(rev:dict):
            msg_type = 'group' if 'group_id' in rev else 'private'
            qq:str = str(rev['user_id']) if 'user_id' in rev else ''
            group_id:str = str(rev['group_id']) if 'group_id' in rev else ''
            num_type:str = qq if msg_type == 'private' else group_id
            rev_msg:str = rev['message'] if 'message' in rev else ''
            return f(msg_type, num_type, rev_msg, qq, rev)
        code = f.__code__
        if not all((
            code.co_argcount == 5,
            code.co_posonlyargcount == 0,
            code.co_kwonlyargcount == 0,
        )):
            raise TypeError("Be careful!")

        if _nickname != None:
            decorator.__nickname__ = _nickname
        if _cmd != None:
            decorator.__cmd__ = _cmd
        return decorator
    return msg_decorator


def grace(_nickname = None, _cmd = None):
    """
    Args:
    ```
        _nickname:str | None : Customized function names
        _cmd:list : The command triggered by the function you added
    ```

    Returns:
    ```
        msg_decorator:'function'
        msg_decorator(f:'function') -> decorator:'function'
        decorator() -> f() | decorator(rev:dict) -> f(rev)
    ```

    Raises:
    ```
        TypeError
    ```

    Examples are as follows:
    ~~~~~~~~~~~~~~~~~~~~~~~~
    ```
    @InsertGroup.manage()
    @grace()
    def _(rev:dict):
        ...
    ```
    or
    ```
    @InsertOthers.manage()
    @grace()
    def _():
        ...
    ```
    """
    def msg_decorator(f:'function'):
        code = f.__code__
        if all((
            code.co_argcount == 0,
            code.co_posonlyargcount == 0,
            code.co_kwonlyargcount == 0,
        )):
            def decorator():
                return f()
        elif all((
            code.co_argcount == 1,
            code.co_posonlyargcount == 0,
            code.co_kwonlyargcount == 0,
        )):
            def decorator(rev:dict):
                return f(rev)
        else:
            raise TypeError("Be careful!")

        if _nickname != None:
            decorator.__nickname__ = _nickname
        if _cmd != None:
            decorator.__cmd__ = _cmd
        return decorator
    return msg_decorator


