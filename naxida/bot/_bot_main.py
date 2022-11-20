import os
import time
import asyncio
import threading

from concurrent.futures import ThreadPoolExecutor

from .insert import (
    Insert,
    InsertIni, InsertSuper,
    InsertPrivate, InsertGroup,
    InsertNotice, InsertRequest,
)
from .charming import Rev
from .config import *
from .manual import *
from .plugin import *
from .receive import *
from .send import *

__all__ = "bot_main",



class Splicing:
    """
    Class Properties:
    ```
        thrust_ini:dict
        thrust_insert:dict
        thrust_super:dict
        thrust_private:dict
        thrust_group:dict
        thrust_notice:dict
        thrust_request:dict

        {
            self_id:str :{
                'xxx':str :['fun':function,],
                ...
            }
        }
    ```
    """
    thrust_ini:dict = {}
    thrust_insert:dict = {}
    thrust_super:dict = {}
    thrust_private:dict = {}
    thrust_group:dict = {}
    thrust_notice:dict = {}
    thrust_request:dict = {}

    @classmethod
    def initialize(cls):
        """Initialization:
        * update class properties `funcfg_dict` and `fun_num_dict`,
          file `funcfg.json`
        * Update all properties in the `Splicing` class that
          start with `thrust_`
        """
        ini_list = [
            'ini', 'insert', 'super',
            'private', 'group', 'notice', 'request',
        ]
        for _ in ini_list: cls._initialize_manual(_)
        for _ in ini_list: cls._initialize_thrust(_)
        asyncio.run(cls._initialize_manage())

    @classmethod
    def _initialize_manual(cls, _insert_type:str):
        """Initialization:
        update class properties `funcfg_dict` and `fun_num_dict`,
        file `funcfg.json`
        """
        if os.path.exists(Config.path_funcfg):
            Manual.renew_funcfg(_insert_type)
            Manual.renew_fun_num(_insert_type)
        else:
            Manual.renew_fun_num(_insert_type)
            if _insert_type == 'private':
                _cp_fun_num_dict = InsertPrivate.fun_num_dict
            elif _insert_type == 'group':
                _cp_fun_num_dict = InsertGroup.fun_num_dict
            elif _insert_type == 'notice':
                _cp_fun_num_dict = InsertNotice.fun_num_dict
            elif _insert_type == 'request':
                _cp_fun_num_dict = InsertRequest.fun_num_dict
            elif _insert_type == 'ini':
                _cp_fun_num_dict = InsertIni.fun_num_dict
            elif _insert_type == 'insert':
                _cp_fun_num_dict = Insert.fun_num_dict
            elif _insert_type == 'super':
                _cp_fun_num_dict = InsertSuper.fun_num_dict

            if _cp_fun_num_dict != {}:
                Manual.renew_by_now(_insert_type)

    @classmethod
    def _initialize_thrust(cls, _insert_type:str):
        """Update all properties in the `Splicing` class that
        start with `thrust_`"""
        if _insert_type == 'private':
            _cp_fun_num_dict = InsertPrivate.fun_num_dict
        elif _insert_type == 'group':
            _cp_fun_num_dict = InsertGroup.fun_num_dict
        elif _insert_type == 'notice':
            _cp_fun_num_dict = InsertNotice.fun_num_dict
        elif _insert_type == 'request':
            _cp_fun_num_dict = InsertRequest.fun_num_dict
        elif _insert_type == 'ini':
            _cp_fun_num_dict = InsertIni.fun_num_dict
        elif _insert_type == 'insert':
            _cp_fun_num_dict = Insert.fun_num_dict
        elif _insert_type == 'super':
            _cp_fun_num_dict = InsertSuper.fun_num_dict

        k:str ; v:dict ; m:str ; n:dict
        _dict = {}
        for m,n in _cp_fun_num_dict.items():
            dict_ = {}
            for k,v in n.items():
                list_ = sorted(
                    v.items(),
                    key = lambda x:x[1], reverse = False
                )
                _list = [i for i in dict(list_).keys()]
                dict_.update({k:_list})
            else:
                _dict.update({m:dict_})
        else:
            for i in list(Config.config_info.keys()):
                if not i in _dict:
                    _dict.update({i:{}})

            if _insert_type == 'private': cls.thrust_private = _dict
            elif _insert_type == 'group': cls.thrust_group = _dict
            elif _insert_type == 'notice': cls.thrust_notice = _dict
            elif _insert_type == 'request': cls.thrust_request = _dict
            elif _insert_type == 'ini': cls.thrust_ini = _dict
            elif _insert_type == 'insert': cls.thrust_insert = _dict
            elif _insert_type == 'super': cls.thrust_super = _dict

    @classmethod
    async def _initialize_manage(cls):
        _to_list = []
        for _ in list(Config.config_info.keys()):
            _dict = cls.thrust_super
            _to_list += _dict.get(_).get('super',[])
            _dict = cls.thrust_private
            _to_list += _dict.get(_).get('private',[])
            _dict = cls.thrust_group
            for i in _dict.get(_).keys():
                _to_list += _dict.get(_).get(i,[])
        rev = {"message":None}
        await asyncio.gather(*[_(rev) for _ in _to_list])


    @classmethod
    def handle_ini(cls):return cls._handle('ini')
    @classmethod
    def handle_insert(cls):return cls._handle('insert')
    @classmethod
    def handle_super(cls,rev):return cls._handle('super',rev)
    @classmethod
    def handle_private(cls,rev):return cls._handle('private',rev)
    @classmethod
    def handle_group(cls,rev):return cls._handle('group',rev)
    @classmethod
    def handle_notice(cls,rev):return cls._handle('notice',rev)
    @classmethod
    def handle_request(cls,rev):return cls._handle('request',rev)

    @classmethod
    def manage_ini(cls):return cls._manage('ini')
    @classmethod
    def manage_insert(cls):return cls._manage('insert')
    @classmethod
    def manage_super(cls,rev):return cls._manage('super',rev)
    @classmethod
    def manage_private(cls,rev):return cls._manage('private',rev)
    @classmethod
    def manage_group(cls,rev):return cls._manage('group',rev)
    @classmethod
    def manage_notice(cls,rev):return cls._manage('notice',rev)
    @classmethod
    def manage_request(cls,rev):return cls._manage('request',rev)


    @classmethod
    async def _process(cls, _insert_type:str, _list:list, rev:dict):
        if _insert_type in ['ini', 'insert']:
            await asyncio.gather(*[_() for _ in _list])

        elif _insert_type in [
            'super', 'private', 'group', 'notice', 'request'
        ]:
            await asyncio.gather(*[_(rev) for _ in _list])

    @classmethod
    def _manage(cls, _insert_type:str, rev:dict = {}):
        self_id = str(rev.get('self_id', None))
        if _insert_type == 'ini': _dict = cls.thrust_ini
        elif _insert_type == 'insert': _dict = cls.thrust_insert
        elif _insert_type == 'super': _dict = cls.thrust_super
        elif _insert_type == 'private': _dict = cls.thrust_private
        elif _insert_type == 'group': _dict = cls.thrust_group
        elif _insert_type == 'notice': _dict = cls.thrust_notice
        elif _insert_type == 'request': _dict = cls.thrust_request

        if _insert_type == 'ini':
            _to_list = list(_dict.values())[0].get(_insert_type,[])
        elif _insert_type == 'insert':
            _to_list = list(_dict.values())[0].get(_insert_type,[])
        elif _insert_type == 'super':
            _to_list = _dict.get(self_id).get(_insert_type,[])
        elif _insert_type == 'private':
            _to_list = _dict.get(self_id).get(_insert_type,[])
        elif _insert_type == 'group':
            _group_id = str(rev.get('group_id'))
            if _group_id in _dict.get(self_id):
                _to_list = _dict.get(self_id).get(_group_id,[])
        elif _insert_type == 'notice':
            _to_list = _dict.get(self_id).get(_insert_type,[])
        elif _insert_type == 'request':
            _to_list = _dict.get(self_id).get(_insert_type,[])

        if _to_list != []:
            asyncio.run(cls._process(_insert_type, _to_list, rev))

    @classmethod
    def _handle(cls, _insert_type:str, rev:dict = {}):
        if _insert_type == 'ini':
            _cp_fun_dict = InsertIni.fun_dict
        elif _insert_type == 'insert':
            _cp_fun_dict = Insert.fun_dict
        elif _insert_type == 'super':
            _cp_fun_dict = InsertSuper.fun_dict
        elif _insert_type == 'private':
            _cp_fun_dict = InsertPrivate.fun_dict
        elif _insert_type == 'group':
            _cp_fun_dict = InsertGroup.fun_dict
        elif _insert_type == 'notice':
            _cp_fun_dict = InsertNotice.fun_dict
        elif _insert_type == 'request':
            _cp_fun_dict = InsertNotice.fun_dict

        if _cp_fun_dict != {}:
            _list = sorted(
                _cp_fun_dict.items(),
                key = lambda x:x[1], reverse = False
            )
            list_ = [l for l,_ in _list]
            if list_ != []:
                asyncio.run(cls._process(_insert_type, list_, rev))



def dealwith_rev(rev:dict):
    """The main handler, which deals with
    `message`, `notice`, `request` and `super` content
    """
    post_type:str = rev['post_type'] if 'post_type' in rev else ''
    msg_type:str = rev['message_type'] if 'message_type' in rev else ''

    _super_bool:bool = all((
        rev.get('user_id') == Config(rev).super_qq,
        any((
            InsertSuper.fun_dict != {},
            InsertSuper.fun_num_dict != {},
        )),
    ))
    if _super_bool:
        if InsertSuper.fun_num_dict != {}: Splicing.manage_super(rev)
        if InsertSuper.fun_dict != {}: Splicing.handle_super(rev)

    if msg_type == 'private':
        _private_bool:bool =all((
            rev.get('user_id') not in Config(rev).blackqq_list,
        ))
        if _private_bool:
            if InsertPrivate.fun_num_dict != {}: Splicing.manage_private(rev)
            if InsertPrivate.fun_dict != {}: Splicing.handle_private(rev)

    elif msg_type == 'group':
        _group_bool:bool = all((
            rev.get('group_id') in Config(rev).group_list,
            rev.get('user_id') not in Config(rev).blackqq_list,
        ))
        if _group_bool:
            if InsertGroup.fun_num_dict != {}: Splicing.manage_group(rev)
            if InsertGroup.fun_dict != {}: Splicing.handle_group(rev)

    elif post_type == 'notice':
        _notice_bool:bool = all((
            any((
                rev.get('user_id') not in Config(rev).blackqq_list,
                rev.get('user_id',None) == None,
            )),
            any((
                rev.get('group_id') in Config(rev).group_list,
                rev.get('group_id',None) == None,
            )),
        ))
        if _notice_bool:
            if InsertNotice.fun_num_dict != {}: Splicing.manage_notice(rev)
            if InsertNotice.fun_dict != {}: Splicing.handle_notice(rev)

    elif post_type == 'request':
        _request_bool:bool = all((
            any((
                rev.get('user_id') not in Config(rev).blackqq_list,
                rev.get('user_id',None) == None,
            )),
            any((
                rev.get('group_id') in Config(rev).group_list,
                rev.get('group_id',None) == None,
            )),
        ))
        if _request_bool:
            if InsertRequest.fun_num_dict != {}: Splicing.manage_request(rev)
            if InsertRequest.fun_dict != {}: Splicing.handle_request(rev)


def rev_receive():
    for _ in Receive.dev_list:
        t = threading.Thread(target=_)
        t.start()


def rev_dispose():
    while True:
        if Receive.rev_list != []:
            rev:dict = Receive.rev_list.pop(0)
            Rev.send_rev(rev)
        else:
            continue

        if all((
            rev != {},
            rev.get('post_type', 'meta_event') != 'meta_event',
        )):
            t = threading.Thread(target=dealwith_rev, args=(rev,))
            t.start()


def connect_gocqhttp() -> bool:
    for _ in list(Config.config_info.keys()): Receive(_).bind()
    connected = False
    _i = 0
    while not connected:
        for _ in list(Config.config_info.keys()):
            try:
                result = Send(_).get_status()
            except:
                print("~~~少女祈祷中~~~")
                time.sleep(1)
                result = {'data':{'online':False}}
            if 'data' in result and result['data']['online']:
                _i += 1
        else:
            if _i != 0:
                connected = True
    else:
        return True



def bot_main(_ciallo = None):
    Splicing.initialize()
    Splicing.handle_ini()
    Splicing.manage_ini()
    if connect_gocqhttp():
        if _ciallo: print(_ciallo)
        else: print('~~~ciallo~~~')
    with ThreadPoolExecutor() as executor:
        executor.submit(rev_receive)
        executor.submit(rev_dispose)
        executor.submit(Splicing.handle_insert)
        executor.submit(Splicing.manage_insert)


