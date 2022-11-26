import re
import asyncio
import inspect

from typing import overload

from .config import *
from .send import *

__all__ = (
    "schedule", "Rev", "Ciallo", "ciallo",
)



def compat_msg(_msg:str, _msg_type:str, _rev) -> str:
    """Make the messages to be sent compatible with
    group chats and private chats

    Args:
    ```
        _msg:str
        _msg_type:str
        _rev:dict | 'Rev' | 'Ciallo' | 'ciallo'
    ```

    Returns:
    ```
        msg:str
    ```

    Raises:
    ```
        AssertionError
    ```
    """
    assert isinstance(_msg, str)
    assert isinstance(_msg_type, str)
    assert isinstance(_rev, (Rev, dict))
    assert _msg_type in ['private', 'group']
    if isinstance(_rev, Rev): rev_dict:dict = _rev.rev
    if isinstance(_rev, dict): rev_dict:dict = _rev
    if _msg_type == "private":
        if _msg.startswith("[CQ:at,qq="):
            msg = _msg.split("]",1)[-1]
            msg = msg.lstrip("\n")
            msg = "@" + rev_dict['sender']['nickname'] + "\n" + msg
            return msg
        elif _msg.startswith("[CQ:reply,id="):
            _, __, msg = _msg.split("]", 2)
            msg = msg.split("]", 1)[-1]
            msg = "@" + rev_dict['sender']['nickname'] + "\n"+ msg
            msg = _ + "]" + __ + "]" + msg
            return msg
    else:
        return _msg



@overload
def grace():...
@overload
def grace(_nickname:str, /):...
@overload
def grace(_nickname:str, _cmd:list, /):...
@overload
def grace(_nickname = None, _cmd = None):...

def grace(_nickname = None, _cmd = None):
    """Elegant

    * Decorate a function to make it look simpler

    Args:
    ```
        _nickname:str | None   :Customized function names
        _cmd:list | None   :The command triggered by the function you added
    ```

    Raises:
    ```
        AssertionError
    ```

    ---
    Examples are as follows:
    ~~~~~~~~~~~~~~~~~~~~~~~~
    ```
    from fnbot import grace
    from fnbot import IstMsg

    @IstMsg.manage()
    @grace()
    async def _(msg_type:str, num_type:str, rev):
        # rev:'Rev' | 'Ciallo' | 'ciallo'
        # msg = 'ciallo'
        # Send(rev).send_msg(msg_type, num_type, msg)
        ...
    ```
    ---
    In terms of results, this is equivalent to the following example,
    but the above is more concise
    ---
    ```
    @InsertMsg.manage()
    @grace()
    async def _(rev): # rev:'Rev' | 'Ciallo' | 'ciallo'
        msg_type = 'group' if 'group_id' in rev else 'private'
        qq:str = str(rev['user_id']) if 'user_id' in rev else ''
        group_id:str = str(rev['group_id']) if 'group_id' in rev else ''
        num_type:str = qq if msg_type == 'private' else group_id
        ...
    ```
    ---
    ... or
    ```
    from fnbot import grace
    from fnbot import IstIni

    @InsertIni.manage()
    @grace()
    async def _():...
    ```
    ---
    ... or
    ```
    from fnbot import grace
    from fnbot import Insert

    @Insert.manage()
    @grace()
    async def _():...
    ```
    """
    assert _nickname == None or isinstance(_nickname, str)
    assert _cmd == None or isinstance(_cmd, list)
    def _decorator(f):
        assert getattr(f.__code__, 'co_argcount', None) in [0, 1, 3]
        assert getattr(f.__code__, 'co_posonlyargcount', None) == 0
        assert getattr(f.__code__, 'co_kwonlyargcount', None) == 0

        if getattr(f.__code__, 'co_argcount', None) == 0:
            async def decorator(): await f()
        elif getattr(f.__code__, 'co_argcount', None) == 1:
            async def decorator(rev:dict): _rev = Rev(rev) ; await f(_rev)
        else:
            async def decorator(rev:dict):
                msg_type:str = 'group' if 'group_id' in rev else 'private'
                qq:str = str(rev['user_id']) if 'user_id' in rev else ''
                group_id = str(rev['group_id']) if 'group_id' in rev else ''
                num_type:str = qq if msg_type == 'private' else group_id
                _rev = Rev(rev)
                await f(msg_type, num_type, _rev)

        if _nickname != None: setattr(decorator, '__nickname__', _nickname)
        if _cmd != None: setattr(decorator, '__cmd__', _cmd)
        return decorator
    return _decorator


def forward_msg(name, uin, msg_list:list) -> list:
    """
    Args:
    ```
        name:str | int
        uin:str | int
        msg_list:list[str]
    ```
    Returns:
    ```
        forward_msg:list
    ```
    """
    assert isinstance(name, (str, int))
    assert isinstance(uin, (str, int))
    assert isinstance(msg_list, list)
    _forward_msg = []
    for msg in msg_list:
        _forward_msg.append(
            {
                "type": "node",
                "data": {
                    "name": str(name),
                    "uin": str(uin),
                    "content": msg
                }
            }
        )
    else:
        return _forward_msg



class Rev:
    """
    Class Properties:
    ```
        objself_list: list[self@Rev]
        pattern_list: list['function']
        _the_pattern_list: list['FullArgSpec':tuple]
    ```

    Instance Properties:
    ```
        rev:dict
        rev_list: list[dict]
        rev_except_list: list['Rev']
        ...
    ```
    """
    __slots__ = (
        "rev", "rev_list", "rev_except_list",
        "time", "self_id", "post_type",
        "message_type", "notice_type", "request_type",

        "card_new", "card_old", "client", "comment", "duration", "file",
        "flag", "font", "group_id", "honor_type", "message", "message_id",
        "online", "operator_id", "raw_message", "sender_id", "sub_type",
        "target_id", "user_id", "sender",

        "sender_age", "sender_nickname", "sender_sex", "sender_user_id",
        "sender_group_id",
        "sender_area", "sender_card", "sender_level", "sender_role",
        "sender_title",
    )
    objself_list:list = []
    """`list[self@Rev]`"""
    pattern_list:list = []
    """`list['function']`"""
    _the_pattern_list:list = []
    """`list['FullArgSpec':tuple]`"""
    def __init__(self, _rev:dict):
        self.rev_list = []
        self.rev_except_list = []
        self.rev = _rev
        self.time = _rev.get('time', None)
        self.self_id = _rev.get('self_id', None)
        self.post_type = _rev.get('post_type', None)

        self.message_type = _rev.get('message_type', None)
        self.notice_type = _rev.get('notice_type', None)
        self.request_type = _rev.get('request_type', None)

        self.card_new = _rev.get("card_new", None)
        self.card_old = _rev.get("card_old", None)
        self.client = _rev.get("client", None)
        self.comment = _rev.get("comment", None)
        self.duration = _rev.get("duration", None)
        self.file = _rev.get("file", None)
        self.flag = _rev.get("flag", None)
        self.font = _rev.get('font', None)
        self.group_id = _rev.get('group_id', None)
        self.honor_type = _rev.get("honor_type", None)
        self.message = _rev.get('message', None)
        self.message_id = _rev.get('message_id', None)
        self.online = _rev.get("online", None)
        self.operator_id = _rev.get("operator_id", None)
        self.raw_message = _rev.get("raw_message", None)
        self.sender_id = _rev.get("sender_id", None)
        self.sub_type = _rev.get('sub_type', None)
        self.target_id = _rev.get("target_id", None)
        self.user_id = _rev.get('user_id', None)

        self.sender:dict = _rev.get('sender', {})
        # sender (in private or group)
        self.sender_age = self.sender.get('age', None)
        self.sender_nickname = self.sender.get('nickname', None)
        self.sender_sex = self.sender.get('sex', None)
        self.sender_user_id = self.sender.get('user_id', None)
        # sender (only in group)
        self.sender_area = self.sender.get('area', None)
        self.sender_card = self.sender.get('card', None)
        self.sender_level = self.sender.get('level', None)
        self.sender_role = self.sender.get('role', None)
        self.sender_title = self.sender.get('title', None)
        # sender (only in temp)
        self.sender_group_id = self.sender.get('group_id', None)

    @property
    def msg_type(self) -> str:
        if self.group_id != None: return self.message_type
        if self.group_id == None: return 'private'
    @property
    def num_type(self):
        if self.group_id != None: return self.group_id
        if self.group_id == None: return self.user_id

    @property
    def msg(self) -> str:
        if self.message == None: return ''
        else: return self.message
    @msg.setter
    def msg(self, _msg:str):
        assert isinstance(_msg, str)
        self.message = _msg

    @property
    def qq(self): return self.user_id
    @property
    def msg_id(self): return self.message_id


    @overload
    def match(self, _equal:list, /) -> bool:...
    @overload
    def match(self, _equal:str, /) -> bool:...
    @overload
    def match(self, *, _search:str) -> bool:...
    @overload
    def match(self, *, _match:str) -> bool:...
    @overload
    def match(self, *, _fullmatch:str) -> bool:...
    @overload
    def match(self, _equal = None, /, *,
        _search:str, _match:str, _fullmatch:str,
    ) -> bool:...
    @overload
    def match(self, _equal = None,
        _search = None, _match = None, _fullmatch = None,
    ) -> bool:...

    def match(self, _equal = None,
        _search = None, _match = None, _fullmatch = None,
    ) -> bool:
        """
        Args:
        ```
            _equal:str | list | None
            _search:str | None   :(re.search(_search, self.msg))
            _match:str | None   :(re.match(_match, self.msg))
            _fullmatch:str | None   :(re.fullmatch(_fullmatch, self.msg))
        ```

        Returns:
        ```
            bool   :any((
                _equal((self.msg == _equal) or (self.msg in _equal)),
                re.search(_search, self.msg),
                re.match(_match, self.msg),
                re.fullmatch(_fullmatch, self.msg)
            ))
        ```

        Raises:
        ```
            AssertionError
        ```
        """
        def _(msg, __equal = _equal,
            __search = _search, __match = _match, __fullmatch = _fullmatch,
        ) -> bool:
            if isinstance(__equal, str): __equal = (msg == __equal)
            if isinstance(__equal, list): __equal = (msg in __equal)
            if __search == None: __search = False
            else: __search = re.search(__search, msg)
            if __match == None: __match = False
            else: __match = re.match(__match, msg)
            if __fullmatch == None: __fullmatch = False
            else: __fullmatch = re.fullmatch(__fullmatch, msg)
            return any((__equal, __search, __match, __fullmatch))

        if inspect.getfullargspec(_) not in self._the_pattern_list:
            self.pattern_list.append(_)
            self._the_pattern_list.append(inspect.getfullargspec(_))
        try: assert isinstance(self.message, str)
        except AssertionError: return False

        assert _equal == None or isinstance(_equal, (str, list))
        assert _search == None or isinstance(_search, str)
        assert _match == None or isinstance(_match, str)
        assert _fullmatch == None or isinstance(_fullmatch, str)
        # _named_tuple = inspect.getfullargspec(self.match)
        # args_list = _named_tuple.args
        # defaults_tuple = _named_tuple.defaults
        # kwonlyargs_list = _named_tuple.kwonlyargs
        # kwonlydefaults_dict = _named_tuple.kwonlydefaults
        if isinstance(_equal, str): _equal = (self.msg == _equal)
        if isinstance(_equal, list): _equal = (self.msg in _equal)
        if _search == None: _search = False
        else: _search = re.search(_search, self.msg)
        if _match == None: _match = False
        else: _match = re.match(_match, self.msg)
        if _fullmatch == None: _fullmatch = False
        else: _fullmatch = re.fullmatch(_fullmatch, self.msg)
        return any((_equal, _search, _match, _fullmatch))


    @classmethod
    def send_rev(cls, _rev:dict):
        if cls.objself_list != []:
            _:'Rev'
            for _ in cls.objself_list:
                if all((
                    _rev.get('self_id', None) != None,
                    _rev.get('user_id', None) != None,
                    _rev.get('message', None) != None,
                    str(_.self_id) == str(_rev.get('self_id', None)),
                )):
                    _.rev_list.append(_rev)


    @overload
    async def awtrev(self) -> 'Rev':...
    @overload
    async def awtrev(self, user_id, /) -> 'Rev':...
    @overload
    async def awtrev(self, user_id, msg_type:str, /) -> 'Rev':...
    @overload
    async def awtrev(self, user_id = None, msg_type = None) -> 'Rev':...

    async def awtrev(self, user_id = None, msg_type = None) -> 'Rev':
        """
        Receive the next rev(msg...) from a specific person
        on a specific occasion

        Args:
        ```
            msg_type:str | None   :('private' or 'group')
            user_id:str | int | None
        ```
        Returns:
        ```
            'Rev' | 'Ciallo' | 'ciallo'
        ```
        """
        assert msg_type == None or isinstance(msg_type, str)
        assert msg_type in ['private', 'group', None]
        assert user_id == None or isinstance(user_id, (str, int))
        while True:
            if self.rev_list != []:
                rev = self.rev_list.pop(0)
                rev = Rev(rev)
                _bool_list:list = [_(rev.msg) for _ in self.pattern_list]
                if user_id == None: user_id = self.user_id
                if _bool_list.count(False) == len(_bool_list):
                    if all((
                        user_id == None, msg_type == None,
                    )):
                        _bool = all((
                            str(user_id) == str(rev.user_id),
                            str(self.group_id) == str(rev.group_id)
                        ))
                    elif all((
                        user_id != None, msg_type == None,
                    )):
                        _bool = all((
                            str(user_id) == str(rev.user_id),
                        ))
                    elif all((
                        user_id != None, msg_type == "private",
                    )):
                        _bool = all((
                            str(user_id) == str(rev.user_id),
                            rev.msg_type == "private",
                        ))
                    elif all((
                        user_id != None, msg_type == "group",
                    )):
                        _bool = all((
                            str(user_id) == str(rev.user_id),
                            rev.msg_type == "group",
                        ))

                    if _bool: return rev
                    else: self.rev_except_list.append(rev)
            await asyncio.sleep(0.1)

    async def awtexcrev(self) -> 'Rev':
        """
        Receive the next rev(msg) from someone
        other than a specific person on a specific occasion

        Returns:
        ```
            'Rev' | 'Ciallo' | 'ciallo'
        ```
        """
        while True:
            if self.rev_except_list != []:
                rev = self.rev_except_list.pop(0)
                return rev
            await asyncio.sleep(0.1)


    @classmethod
    def compat_msg(cls, _msg:str, _msg_type:str, _rev) -> str:
        """
        Make the messages to be sent compatible with
        group chats and private chats

        Args:
        ```
            _msg:str
            _msg_type:str
            _rev:dict | 'Rev' | 'Ciallo' | 'ciallo'
        ```

        Returns:
        ```
            msg:str
        ```

        Raises:
        ```
            AssertionError
        ```
        """
        assert isinstance(_msg, str)
        assert isinstance(_msg_type, str)
        assert isinstance(_rev, (Rev, dict))
        assert _msg_type in ['private', 'group']
        return compat_msg(_msg, _msg_type, _rev)


    @overload
    @classmethod
    def grace(cls):...
    @overload
    @classmethod
    def grace(cls, _nickname:str, /):...
    @overload
    @classmethod
    def grace(cls, _nickname:str, _cmd:list, /):...
    @overload
    @classmethod
    def grace(cls, _nickname = None, _cmd = None):...

    @classmethod
    def grace(cls, _nickname = None, _cmd = None):
        """Elegant

        * Decorate a function to make it look simpler

        Args:
        ```
            _nickname:str | None   :Customized function names
            _cmd:list | None   :The command triggered by the function you added
        ```

        Raises:
        ```
            AssertionError
        ```

        ---
        Examples are as follows:
        ~~~~~~~~~~~~~~~~~~~~~~~~
        ```
        from fnbot import Rev
        from fnbot import IstMsg

        @IstMsg.manage()
        @Rev.grace()
        async def _(msg_type:str, num_type:str, rev:'Rev'):
            # msg = 'ciallo'
            # Send(rev).send_msg(msg_type, num_type, msg)
            ...
        ```
        ---
        In terms of results, this is equivalent to the following example,
        but the above is more concise
        ---
        ```
        @InsertMsg.manage()
        @Rev.grace()
        async def _(rev:'Rev'):
            msg_type = 'group' if 'group_id' in rev else 'private'
            qq:str = str(rev['user_id']) if 'user_id' in rev else ''
            group_id:str = str(rev['group_id']) if 'group_id' in rev else ''
            num_type:str = qq if msg_type == 'private' else group_id
            ...
        ```
        ---
        ... or
        ```
        from fnbot import grace
        from fnbot import IstIni

        @InsertIni.manage()
        @Rev.grace()
        async def _():...
        ```
        ---
        ... or
        ```
        from fnbot import grace
        from fnbot import Insert

        @Insert.manage()
        @Rev.grace()
        async def _():...
        ```
        """
        assert _nickname == None or isinstance(_nickname, str)
        assert _cmd == None or isinstance(_cmd, list)
        return grace(_nickname, _cmd)


    @overload
    @classmethod
    def forward_msg(cls, name:str, uin:int, msg_list:list, /) -> list:...
    @overload
    @classmethod
    def forward_msg(cls, name:int, uin:str, msg_list:list, /) -> list:...
    @overload
    @classmethod
    def forward_msg(cls, name:str, uin:str, msg_list:list, /) -> list:...
    @overload
    @classmethod
    def forward_msg(cls, name:int, uin:int, msg_list:list, /) -> list:...

    @classmethod
    def forward_msg(cls, name, uin, msg_list:list) -> list:
        """
        Args:
        ```
            name:str | int
            uin:str | int
            msg_list:list[str]
        ```
        Returns:
        ```
            forward_msg:list
        ```
        """
        assert isinstance(name, (str, int))
        assert isinstance(uin, (str, int))
        assert isinstance(msg_list, list)
        return forward_msg(name, uin, msg_list)


    @classmethod
    def current_dev(cls) -> list:
        dev_list = []
        for _ in list(Config.config_info.keys()):
            try:
                result = Send(_).get_status()
            except:
                result = {'data':{'online':False}}
            if 'data' in result and result['data']['online']:
                dev_list.append(_)
        return dev_list


    def identify_privilege(self,
        _group:bool = False, _toml:bool = False,
    ) -> bool:
        """Identify if you have privilege

        Args:
        ```
            _group:bool   :Whether to include group owners and administrators
            _toml:bool   :Whether to include the `admin_list`
                          in the file `pybot.toml`
        ```
        Returns:
        ```
            bool
        ```
        """
        assert _group == False or isinstance(_group, bool)
        assert _toml == False or isinstance(_toml, bool)
        if any((self.self_id == None, self.user_id == None)): return False
        if all((_group == False, _toml == False,)):
            return any((
                int(self.user_id) == Config(self.self_id).super_qq
            ))
        elif all((_group == True, _toml == False,)):
            if self.group_id != None:
                role = Send(self.self_id).get_group_member_info(
                    self.group_id, self.user_id
                )
            else: role = ''
            if 'data' in role: role = role['data']
            if 'role' in role: role = role['role']
            if not isinstance(role, str): role = ''
            return any((
                role in ['admin', 'owner'],
                int(self.user_id) == Config(self.self_id).super_qq,
            ))
        elif all((_group == True, _toml == True,)):
            if self.group_id != None:
                role = Send(self.self_id).get_group_member_info(
                    self.group_id, self.user_id
                )
            else: role = ''
            if 'data' in role: role = role['data']
            if 'role' in role: role = role['role']
            if not isinstance(role, str): role = ''
            return any((
                role in ['admin', 'owner'],
                self.user_id in Config(self.self_id).admin_list,
                int(self.user_id) == Config(self.self_id).super_qq,
            ))


    def isexcept(self, _msg:str) -> bool:
        assert isinstance(_msg, str)
        _bool_list:list = [_(_msg) for _ in self.pattern_list]
        if _bool_list.count(False) == len(_bool_list): return True
        else: return False

class Ciallo(Rev):pass
class ciallo(Rev):
    """a few
    ```
    @IstMsg.manage()
    @ciallo.grace()
    async def _(msg_type:str, num_type:str, rev:'ciallo'):
        msg = 'ciallo'
        Send(rev).send_msg(msg_type, num_type, msg)

        msg_list = ['ciallo']
        msg = ciallo.forward_msg(rev.time, rev.self_id, msg_list)
        Send(rev).send_forward_msg(msg_type, num_type, msg)

    @InsertMsg.manage()
    @ciallo.grace()
    async def _(rev:'ciallo'):
    ```
    ---
    Usages:
    ~~~~~~~
    * Use `ciallo.grace()` to decorate a coroutine
    * Use `ciallo.compat_msg(...) ` to fix the effect of message
      sent to a group message that are sent to a private message
    * Use `ciallo.forward_msg(...)` to get the prescribed merge
      forwarding message
    * Use `ciallo.current_dev()` to get a running device
    * Use `self@ciallo.match(...) ` to match the incoming message
    * Use `self@ciallo.identify_privilege(...) ` to see whether
      the appropriate permissions are available
    * Use `self@ciallo.isexcept(...) ` to see whether the pattern
      will match successfully in existing patterns
    * Use `await self@ciallo.awtrev()` to get a news for the next event loop
    * Use `await self@ciallo.awtexcrev()` to get an otherwise unsolicited
      message in a later event loop
    ---

    plugin file path

    ```
    import os

    _path = os.path.realpath(__file__)
    _path = _path.rstrip(os.path.basename(__file__))
    _path = eval(repr(_path).replace('\\\\','/'))
    _path = str(_path).rstrip('\\\\').rstrip('/')
    ```
    """



class schedule:
    """
    Args:
    ```
        _awtstart:'coroutine'   :(Should raise an error)
        _awtwait:'coroutine'
        _awtdecline:'coroutine'   :(Should raise an error)
    ```
    ---
    Usages:
    ~~~~~~~
    * Use `await self@schedule.modify(...)` to change the time at which
      the scheduled task must eventually end
    * Use `await self@schedule.cancel()` to actively end scheduled tasks
    * Use `await self@schedule.start(...)` to start a scheduled task

    Examples are as follows:
    ~~~~~~~~~~~~~~~~~~~~~~~~
    ```
    from fnbot import Rev
    from fnbot import IstMsg
    from fnbot import Send
    from fnbot import schedule

    @IstMsg.manage()
    @Rev.grace('/...')
    async def _(msg_type:str, num_type:str, rev:'Rev'):
        if rev.match([...]):
            msg = ...
            Send(rev).send_msg(msg_type, num_type, msg)

            @schedule
            async def task():
                while True:
                    _rev = await rev.awtrev()
                    if _rev.msg in [...]:
                        msg = ...
                        Send(rev).send_msg(msg_type, num_type, msg)
                        await task.cancel()
                    else:
                        msg = ...
                        Send(rev).send_msg(msg_type, num_type, msg)

            @task.awtwait
            async def task():
                while True:
                    _rev = await rev.awtexcrev()
                    if _rev.msg in [...]:
                        msg = ...
                        Send(rev).send_msg(msg_type, num_type, msg)

            @task.awtdecline
            async def task():
                await asyncio.sleep(666)
                msg = ...
                Send(rev).send_msg(msg_type, num_type, msg)
                await task.cancel()
            await task.start(rev)
    ```
    """
    def __init__(self, _awtstart=None, _awtwait=None, _awtdecline=None):
        self._t = 666
        if _awtstart != None: self.__awtstart__ = _awtstart
        if _awtwait != None: self.__awtwait__ = _awtwait
        if _awtdecline != None: self.__awtdecline__ = _awtdecline
    async def __awtstart__(self):...
    async def __awtwait__(self):...
    async def __awtdecline__(self):...
    async def __forever__(self):lambda:...
    async def __death__(self):
        await asyncio.sleep(self._t) ; raise RuntimeError
    async def __run__(self, rev:'Rev'):
        assert isinstance(rev, (Rev, Ciallo, ciallo))
        Rev.objself_list.append(rev)
        try:
            await asyncio.wait(
                (
                    self.__awtstart__(), self.__awtwait__(),
                    self.__awtdecline__(), self.__death__(),
                ),
                return_when = 'FIRST_EXCEPTION',
            )
        finally:
            if rev in Rev.objself_list: Rev.objself_list.remove(rev)
    def awtstart(self, _coro = ...) -> 'schedule':
        assert getattr(_coro.__code__, "co_flags", None) in [147, 195]
        self.__awtstart__ = _coro ; return self
    def awtwait(self, _coro = ...) -> 'schedule':
        assert getattr(_coro.__code__, "co_flags", None) in [147, 195]
        self.__awtwait__ = _coro ; return self
    def awtdecline(self, _coro = ...) -> 'schedule':
        assert getattr(_coro.__code__, "co_flags", None) in [147, 195]
        self.__awtdecline__ = _coro ; return self
    async def modify(self, _t:int): self._t = _t
    async def cancel(self): raise RuntimeError
    async def forever(self): self.__death__ = self.__forever__
    async def start(self, rev:'Rev'): await self.__run__(rev)


