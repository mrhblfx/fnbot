import re
import asyncio
import inspect

from typing import overload

__all__ = (
    "compat_msg", "grace",
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
        if msg.startswith("[CQ:at,qq="):
            msg = msg.split("]",1)[-1]
            msg = msg.lstrip("\n")
            msg = "@" + rev_dict['sender']['nickname'] + "\n" + msg
            return msg
        elif msg.startswith("[CQ:reply,id="):
            _, __, msg = msg.split("]",2)
            msg = msg.split("]",1)[-1]
            msg = "@" + rev_dict['sender']['nickname'] + msg
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
    from naxida import grace
    from naxida import IstMsg

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
    from naxida import grace
    from naxida import IstIni

    @InsertIni.manage()
    @grace()
    async def _():...
    ```
    ---
    ... or
    ```
    from naxida import grace
    from naxida import Insert

    @Insert.manage()
    @grace()
    async def _():...
    ```
    """
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
        "sub_type", "message_id", "user_id", "group_id",
        "message", "raw_message", "font",
        "nickname", "sex", "age",
        "card", "area", "level", "role", "title",
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
        self.sub_type = _rev.get('sub_type', None)
        self.message_id = _rev.get('message_id', None)
        self.user_id = _rev.get('user_id', None)
        self.group_id = _rev.get('group_id', None)
        self.message:str = _rev.get('message', '')
        self.raw_message = _rev.get('raw_message', None)
        self.font = _rev.get('font', None)
        # sender (in private or group)
        self.nickname = getattr(_rev.get('sender', None), 'nickname', None)
        self.sex = getattr(_rev.get('sender', None), 'sex', None)
        self.age = getattr(_rev.get('sender', None), 'age', None)
        # sender (only in group)
        self.card = getattr(_rev.get('sender', None), 'card', None)
        self.area = getattr(_rev.get('sender', None), 'area', None)
        self.level = getattr(_rev.get('sender', None), 'level', None)
        self.role = getattr(_rev.get('sender', None), 'role', None)
        self.title = getattr(_rev.get('sender', None), 'title', None)

        self.notice_type = _rev.get('notice_type', None)
        self.request_type = _rev.get('request_type', None)

    @property
    def msg_type(self) -> str:
        if self.group_id != None: return self.message_type
        if self.group_id == None: return 'private'
    @property
    def num_type(self):
        if self.group_id != None: return self.group_id
        if self.group_id == None: return self.user_id
    @property
    def msg(self) -> str: return self.message
    @property
    def qq(self): return self.user_id


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
            bool   :self.msg == _equal(str) or
                    self.msg in _equal(list)
            bool   :any((
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
            if __equal != None:
                if isinstance(__equal, str): return msg == __equal
                if isinstance(__equal, list): return msg in __equal
            else:
                if __search == None: __search = False
                else: __search = re.search(__search, msg)
                if __match == None: __match = False
                else: __match = re.match(__match, msg)
                if __fullmatch == None: __fullmatch = False
                else: __fullmatch = re.fullmatch(__fullmatch, msg)
                return any((__search, __match, __fullmatch))

        if inspect.getfullargspec(_) not in self._the_pattern_list:
            self.pattern_list.append(_)
            self._the_pattern_list.append(inspect.getfullargspec(_))
        try: assert type(self.msg) == str
        except AssertionError: return False

        assert _equal == None or isinstance(_equal, (str, list))
        assert _search == None or isinstance(_search, str)
        assert _match == None or isinstance(_match, str)
        assert _fullmatch == None or isinstance(_fullmatch, str)
        _named_tuple = inspect.getfullargspec(self.match)
        # args_list = _named_tuple.args
        defaults_tuple = _named_tuple.defaults
        # kwonlyargs_list = _named_tuple.kwonlyargs
        # kwonlydefaults_dict = _named_tuple.kwonlydefaults
        if _equal not in defaults_tuple:
            if isinstance(_equal, str): return self.msg == _equal
            if isinstance(_equal, list): return self.msg in _equal
        else:
            if _search == None: _search = False
            else: _search = re.search(_search, self.msg)
            if _match == None: _match = False
            else: _match = re.match(_match, self.msg)
            if _fullmatch == None: _fullmatch = False
            else: _fullmatch = re.fullmatch(_fullmatch, self.msg)
            return any((_search, _match, _fullmatch))


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

    async def awtrev(self) -> 'Rev':
        """
        Receive the next rev(msg...) from a specific person
        on a specific occasion

        Returns:
        ```
            'Rev' | 'Ciallo' | 'ciallo'
        ```
        """
        while True:
            if self.rev_list != []:
                rev = self.rev_list.pop(0)
                rev = Rev(rev)
                _bool_list:list = [_(rev.msg) for _ in self.pattern_list]
                if _bool_list.count(False) == len(_bool_list):
                    if all((
                        str(self.user_id) == str(rev.user_id),
                        str(self.group_id) == str(rev.group_id),
                    )):
                        return rev
                    else:
                        self.rev_except_list.append(rev)
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
        from naxida import Rev
        from naxida import IstMsg

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
        from naxida import grace
        from naxida import IstIni

        @InsertIni.manage()
        @Rev.grace()
        async def _():...
        ```
        ---
        ... or
        ```
        from naxida import grace
        from naxida import Insert

        @Insert.manage()
        @Rev.grace()
        async def _():...
        ```
        """
        return grace(_nickname, _cmd)

class Ciallo(Rev):pass
class ciallo(Rev):pass



class schedule:
    """
    Args:
    ```
        _awtstart:'coroutine'   :(Should raise an error)
        _awtwait:'coroutine'
        _awtdecline:'coroutine'   :(Should raise an error)
    ```

    ---
    Examples are as follows:
    ~~~~~~~~~~~~~~~~~~~~~~~~
    ```
    import time
    from naxida import ciallo
    from naxida import IstMsg

    @IstMsg.manage()
    @ciallo.grace('/...')
    async def _(msg_type:str, num_type:str, rev:'ciallo'):
        if rev.match(["..."]):
            msg = ...
            Send(rev).send_msg(msg_type, num_type, msg)

            @schedule
            async def task():
                while True:
                    _rev = await rev.awtrev()
                    if _rev.msg == '...':
                        msg = '...'
                        Send(rev).send_msg(msg_type, num_type, msg)
                        raise RuntimeError
                    else:
                        msg = '...'
                        Send(rev).send_msg(msg_type, num_type, msg)

            @task.awtwait
            async def task():
                while True:
                    _rev = await rev.awtexcrev()
                    if _rev.msg == '...':
                        msg = '...'
                        Send(rev).send_msg(msg_type, num_type, msg)
                    await asyncio.sleep(1)

            @task.awtdecline
            async def task():
                start_time = time.monotonic()
                end_time = start_time + 666
                while True:
                    if (time.monotonic() + 1.0) >= end_time:
                        msg = ...
                        Send(rev).send_msg(msg_type, num_type, msg)
                        raise RuntimeError
                    await asyncio.sleep(666)
            await task.run(rev)
    ```
    """
    def __init__(self, _awtstart=None, _awtwait=None, _awtdecline=None):
        if _awtstart != None: self.__awtstart__ = _awtstart
        if _awtwait != None: self.__awtwait__ = _awtwait
        if _awtdecline != None: self.__awtdecline__ = _awtdecline
    def awtstart(self, _coro) -> 'schedule':
        self.__awtstart__ = _coro ; return self
    def awtwait(self, _coro) -> 'schedule':
        self.__awtwait__ = _coro ; return self
    def awtdecline(self, _coro) -> 'schedule':
        self.__awtdecline__ = _coro ; return self
    async def __awtstart__(self):...
    async def __awtwait__(self):...
    async def __awtdecline__(self):...
    async def __death__(self, _t:int = 666):
        await asyncio.sleep(_t)
        raise RuntimeError
    async def __run__(self, rev:'Rev'):
        Rev.objself_list.append(rev)
        try:
            await asyncio.wait(
                (
                    self.__awtstart__(), self.__awtwait__(),
                    self.__awtdecline__(), self.__death__(),
                ),
                return_when='FIRST_EXCEPTION',
            )
        finally:
            if rev in Rev.objself_list:
                Rev.objself_list.remove(rev)
    async def run(self, rev:'Rev'): await self.__run__(rev)


