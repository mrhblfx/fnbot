import os
import time
import json
import traceback
import threading

from  concurrent.futures import ThreadPoolExecutor

from .insert import *
from .manual import *
from .plugin import *
from .send import *
from .receive import *
from .config import *

__all__ = (
    "bot_main", "logerr",
)

def logerr(rev:str = ''):
    """Logging errors

    Generate `ErrorLog.txt` file in the working directory by default
    when an error is encountered

    Args:
        `rev:str (Default: '' )`
    """
    if rev != "":
        rev = json.dumps(
            rev , sort_keys=True ,
            indent=4 , separators=(',', ':') ,
            ensure_ascii=False
        )

    file_path = Config.path_pybot + '/ErrorLog.txt'
    if os.path.exists(file_path):
        with open(file_path, "a", encoding="utf-8") as f:
            f.write("\n")
            f.write(time.strftime("%Y-%m-%d %H:%M:%S"))
            f.write("\n")
            f.write(rev)
            f.write("\n")
            f.write(f"{traceback.format_exc()}")
            f.write("\n")
            f.write("="*69)
    else:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n")
            f.write(time.strftime("%Y-%m-%d %H:%M:%S"))
            f.write("\n")
            f.write(rev)
            f.write("\n")
            f.write(f"{traceback.format_exc()}")
            f.write("\n")
            f.write("="*69)


class Splicing:
    """
    Class Properties:
    ```
        thrust_ini:dict
        thrust_others:dict
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
    thrust_others:dict = {}
    thrust_super:dict = {}
    thrust_private:dict = {}
    thrust_group:dict = {}
    thrust_notice:dict = {}
    thrust_request:dict = {}

    @classmethod
    def init_ini(cls):
        """Initialization:
        * update class properties `funcfg_dict` and `fun_num_dict`,
          file `funcfg.json`
        * Update all properties in the `Splicing` class that
          start with `thrust_`
        """
        cls._initialize_manual('private')
        cls._initialize_manual('group')
        cls._initialize_manual('notice')
        cls._initialize_manual('request')
        cls._initialize_manual('ini')
        cls._initialize_manual('others')
        cls._initialize_manual('super')
        cls._renew_thrust('private')
        cls._renew_thrust('group')
        cls._renew_thrust('notice')
        cls._renew_thrust('request')
        cls._renew_thrust('ini')
        cls._renew_thrust('others')
        cls._renew_thrust('super')
        cls._handle('ini')
        cls._manage('ini')


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
            elif _insert_type == 'others':
                _cp_fun_num_dict = InsertOthers.fun_num_dict
            elif _insert_type == 'super':
                _cp_fun_num_dict = InsertSuper.fun_num_dict

            if _cp_fun_num_dict != {}:
                Manual.renew_by_now(_insert_type)


    @classmethod
    def _renew_thrust(cls, _insert_type:str):
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
        elif _insert_type == 'others':
            _cp_fun_num_dict = InsertOthers.fun_num_dict
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

            if _insert_type == 'private':
                cls.thrust_private = _dict
            elif _insert_type == 'group':
                cls.thrust_group = _dict
            elif _insert_type == 'notice':
                cls.thrust_notice = _dict
            elif _insert_type == 'request':
                cls.thrust_request = _dict
            elif _insert_type == 'ini':
                cls.thrust_ini = _dict
            elif _insert_type == 'others':
                cls.thrust_others = _dict
            elif _insert_type == 'super':
                cls.thrust_super = _dict


    @classmethod
    def _process(cls, _insert_type:str, _list:list, rev:dict):
        if _insert_type == 'ini':
            for _ in _list:
                try:
                    _()
                except TypeError:
                    raise TypeError("Be careful!")

        elif _insert_type == 'others':
            for _ in _list:
                try:
                    t = threading.Thread(target=_)
                    t.start()
                except TypeError:
                    raise TypeError("Be careful!")

        elif _insert_type in [
            'super', 'private', 'group', 'notice', 'request'
        ]:
            for _ in _list:
                try:
                    _(rev)
                except TypeError:
                    raise TypeError("Be careful!")


    @classmethod
    def _manage(cls, _insert_type:str, rev:dict = {}):
        self_id = str(rev.get('self_id',0))
        if _insert_type == 'ini':
            _dict = cls.thrust_ini
        elif _insert_type == 'others':
            _dict = cls.thrust_others
        elif _insert_type == 'super':
            _dict = cls.thrust_super
        elif _insert_type == 'private':
            _dict = cls.thrust_private
        elif _insert_type == 'group':
            _dict = cls.thrust_group
        elif _insert_type == 'notice':
            _dict = cls.thrust_notice
        elif _insert_type == 'request':
            _dict = cls.thrust_request

        if _insert_type == 'ini':
            _to_list = list(_dict.values())[0].get(_insert_type,[])
        elif _insert_type == 'others':
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
            cls._process(_insert_type, _to_list, rev)


    @classmethod
    def _handle(cls, _insert_type:str, rev:dict = {}):
        if _insert_type == 'ini':
            _cp_fun_dict = InsertIni.fun_dict
        elif _insert_type == 'others':
            _cp_fun_dict = InsertOthers.fun_dict
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
                cls._process(_insert_type, list_, rev)


def dealwith(rev:dict):
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
        if InsertSuper.fun_num_dict != {}:
            Splicing._manage('super', rev,)
        if InsertSuper.fun_dict != {}:
            Splicing._handle('super', rev,)

    if msg_type == 'private':
        _private_bool:bool =all((
            rev.get('user_id') not in Config(rev).blackqq_list,
        ))
        if _private_bool:
            if InsertPrivate.fun_num_dict != {}:
                Splicing._manage('private', rev,)
            if InsertPrivate.fun_dict != {}:
                Splicing._handle('private', rev,)

    elif msg_type == 'group':
        _group_bool:bool = all((
            rev.get('group_id') in Config(rev).group_list,
            rev.get('user_id') not in Config(rev).blackqq_list,
        ))
        if _group_bool:
            if InsertGroup.fun_num_dict != {}:
                Splicing._manage('group', rev)
            if InsertGroup.fun_dict != {}:
                Splicing._handle('group', rev,)

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
            if InsertNotice.fun_num_dict != {}:
                Splicing._manage('notice', rev,)
            if InsertNotice.fun_dict != {}:
                Splicing._handle('notice', rev,)

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
            if InsertRequest.fun_num_dict != {}:
                Splicing._manage('request', rev,)
            if InsertRequest.fun_dict != {}:
                Splicing._handle('request', rev,)


def rev_receive():
    for _ in Receive.dev_list:
        t = threading.Thread(target=_)
        t.start()


def rev_dispose():
    while True:
        if Receive.rev_list != []:
            rev = Receive.rev_list.pop(0)
        else:
            rev = {}

        if rev != {}:
            if rev.get('post_type') != 'meta_event':
                t = threading.Thread(target=dealwith, args=(rev,))
                t.start()


def connect_gocqhttp() -> bool:
    for i in list(Config.config_info.keys()):
        Receive(i).bind()
    connected = False
    _ = 0
    while not connected:
        try:
            for i in list(Config.config_info.keys()):
                try:
                    result = Send(i).get_status()
                except:
                    result = {'data':{'online':False}}
                if 'data' in result and result['data']['online']:
                    _ += 1
            else:
                if _ != 0:
                    connected = True
        except:
            print("~~~少女祈祷中~~~")
            time.sleep(1)
    else:
        return True


def bot_main():
    Splicing.init_ini()
    if connect_gocqhttp():
        print("~~~ciallo~~~")
        with ThreadPoolExecutor() as executor:
            executor.submit(Splicing._handle,'others')
            executor.submit(Splicing._manage,'others')
            executor.submit(rev_receive)
            executor.submit(rev_dispose)


