import os
import json

from .insert import *
from .config import *

__all__ = "Manual",

class Manual():
    @classmethod
    def renew_funcfg(cls, _insert_type:str):
        """update class properties `funcfg_dict`,
        file `funcfg.json`

        The file `funcfg.json` must exist

        Args:
        ```
            _insert_type:str in [
                'private', 'group', 'notice', 'request',
                'ini', 'others', 'super',
            ]
        ```

        Returns:
        ```
            None
        ```

        Raises:
        ```
            TypeError: if _insert_type not in [...]
        ```
        """
        with open(Config.path_funcfg, mode='r', encoding="utf-8") as f:
            _f_funcfg:dict = json.load(f)

        if _insert_type == 'private':
            _cp_funcfg_dict:dict = InsertPrivate.funcfg_dict
        elif _insert_type == 'group':
            _cp_funcfg_dict:dict = InsertGroup.funcfg_dict
        elif _insert_type == 'notice':
            _cp_funcfg_dict:dict = InsertNotice.funcfg_dict
        elif _insert_type == 'request':
            _cp_funcfg_dict:dict = InsertRequest.funcfg_dict
        elif _insert_type == 'ini':
            _cp_funcfg_dict:dict = InsertIni.funcfg_dict
        elif _insert_type == 'others':
            _cp_funcfg_dict:dict = InsertOthers.funcfg_dict
        elif _insert_type == 'super':
            _cp_funcfg_dict:dict = InsertSuper.funcfg_dict
        else:
            raise TypeError("Be careful!")

        kk:str ; vv:dict ; _kk:str ; _vv:dict
        _funcfg = {}
        _ist = {}
        for kk,vv in _f_funcfg.items():
            for _kk,_vv in _cp_funcfg_dict.items():
                if kk == _kk:
                    if _insert_type == 'group':
                        _bu = {str(i):{} for i in Config(kk).group_list}
                        _f_:dict = vv.get(_insert_type,_bu)
                    elif _insert_type != 'group':
                        _f_:dict = {_insert_type:vv.get(_insert_type,{})}
            # _f_ | _vv :{_insert_type:{...}} or {group_id:{...},...}
            # k | m : _insert_type or group_id
            # v | n : {fun_name:_bool}
            # _k | _m : fun_name
            # _v | _n : _bool
                    k:str; v:dict; m:str; n:dict
                    _m:str; _n:bool; _k:str; _v:bool
                    for k,v in _f_.items():
                        for m,n in _vv.items():
                            if k == m:
                                for _m,_n in n.items():
                                    if not _m in v:
                                        v.update({_m:_n})
                                    for _k,_v in v.items():
                                        if _k == _m and _v != _n:
                                            n.update({_k:_v})
                                else:
                                    _vv.update({m:n})
                        else:
                            _f_.update({k:v})
                    else:
                        if _insert_type == 'private':
                            vv.update(_f_)
                        elif _insert_type == 'group':
                            vv.update({_insert_type:_f_})
                        elif _insert_type == 'notice':
                            vv.update(_f_)
                        elif _insert_type == 'request':
                            vv.update(_f_)
                        elif _insert_type == 'ini':
                            vv.update(_f_)
                        elif _insert_type == 'others':
                            vv.update(_f_)
                        elif _insert_type == 'super':
                            vv.update(_f_)

                        _ist.update({_kk:_vv})
            else:
                _funcfg.update({kk:vv})
        else:
            with open(Config.path_funcfg, mode='w', encoding="utf-8") as f:
                json.dump(
                    _funcfg, f, sort_keys=True,
                    indent=4, separators=(',', ':'),
                    ensure_ascii=False,
                )
            if _insert_type == 'private':
                InsertPrivate.funcfg_dict = _ist
            elif _insert_type == 'group':
                InsertGroup.funcfg_dict = _ist
            elif _insert_type == 'notice':
                InsertNotice.funcfg_dict = _ist
            elif _insert_type == 'request':
                InsertRequest.funcfg_dict = _ist
            elif _insert_type == 'ini':
                InsertIni.funcfg_dict = _ist
            elif _insert_type == 'others':
                InsertOthers.funcfg_dict = _ist
            elif _insert_type == 'super':
                InsertSuper.funcfg_dict = _ist


    @classmethod
    def renew_fun_num(cls, _insert_type:str):
        """update class properties `fun_num_dict`

        Args:
        ```
            _insert_type:str in [
                'private', 'group', 'notice', 'request',
                'ini', 'others', 'super',
            ]
        ```

        Returns:
        ```
            None
        ```

        Raises:
        ```
            TypeError: if _insert_type not in [...]
        ```
        """
        if _insert_type == 'private':
            _cp_funcfg_dict:dict = InsertPrivate.funcfg_dict
            _cp_fun_info:dict = InsertPrivate.fun_name_info
        elif _insert_type == 'group':
            _cp_funcfg_dict:dict = InsertGroup.funcfg_dict
            _cp_fun_info:dict = InsertGroup.fun_name_info
        elif _insert_type == 'notice':
            _cp_funcfg_dict:dict = InsertNotice.funcfg_dict
            _cp_fun_info:dict = InsertNotice.fun_name_info
        elif _insert_type == 'request':
            _cp_funcfg_dict:dict = InsertRequest.funcfg_dict
            _cp_fun_info:dict = InsertRequest.fun_name_info
        elif _insert_type == 'ini':
            _cp_funcfg_dict:dict = InsertIni.funcfg_dict
            _cp_fun_info:dict = InsertIni.fun_name_info
        elif _insert_type == 'others':
            _cp_funcfg_dict:dict = InsertOthers.funcfg_dict
            _cp_fun_info:dict = InsertOthers.fun_name_info
        elif _insert_type == 'super':
            _cp_funcfg_dict:dict = InsertSuper.funcfg_dict
            _cp_fun_info:dict = InsertSuper.fun_name_info
        else:
            raise TypeError("Be careful!")

        kk:str ; vv:dict ; m:str ; n:dict
        _fun_num_dict:dict = {}
        for kk,vv in _cp_funcfg_dict.items():
            _fun_num = {}
            for m,n in vv.items():
                _fun_name_true:list = [k for k,v in n.items() if v == True]
                for i in _fun_name_true:
                    _info:dict = _cp_fun_info.get(i,{})
                    if _info.get('function',None) != None:
                        _in_v:dict = _fun_num.get(m,{})
                        _in_v.update({_info.get('function'):_info.get('num')})
                        _fun_num.update({m:_in_v})
            else:
                _fun_num_dict.update({kk:_fun_num})
        else:
            if _insert_type == 'private':
                InsertPrivate.fun_num_dict = _fun_num_dict
            elif _insert_type == 'group':
                InsertGroup.fun_num_dict = _fun_num_dict
            elif _insert_type == 'notice':
                InsertNotice.fun_num_dict = _fun_num_dict
            elif _insert_type == 'request':
                InsertRequest.fun_num_dict = _fun_num_dict
            elif _insert_type == 'ini':
                InsertIni.fun_num_dict = _fun_num_dict
            elif _insert_type == 'others':
                InsertOthers.fun_num_dict = _fun_num_dict
            elif _insert_type == 'super':
                InsertSuper.fun_num_dict = _fun_num_dict


    @classmethod
    def renew_by_now(cls, _insert_type:str):
        """Partially rewrite the file `funcfg.json` based on
        the class property `funcfg_dict`

        Args:
        ```
            _insert_type:str in [
                'private', 'group', 'notice', 'request',
                'ini', 'others', 'super',
            ]
        ```

        Returns:
        ```
            None
        ```

        Raises:
        ```
            TypeError: if _insert_type not in [...]
        ```
        """
        if os.path.exists(Config.path_funcfg):
            with open(Config.path_funcfg, mode='r', encoding="utf-8") as f:
                _f_funcfg:dict = json.load(f)
        else:
            _f_funcfg = {str(i):{} for i in list(Config.config_info.keys())}

        if _insert_type == 'private':
            _cp_funcfg_dict:dict = InsertPrivate.funcfg_dict
        elif _insert_type == 'group':
            _cp_funcfg_dict:dict = InsertGroup.funcfg_dict
        elif _insert_type == 'notice':
            _cp_funcfg_dict:dict = InsertNotice.funcfg_dict
        elif _insert_type == 'request':
            _cp_funcfg_dict:dict = InsertRequest.funcfg_dict
        elif _insert_type == 'ini':
            _cp_funcfg_dict:dict = InsertIni.funcfg_dict
        elif _insert_type == 'others':
            _cp_funcfg_dict:dict = InsertOthers.funcfg_dict
        elif _insert_type == 'super':
            _cp_funcfg_dict:dict = InsertSuper.funcfg_dict
        else:
            raise TypeError("Be careful!")

        k:str ; v:dict ; m:str ; n:dict
        _funcfg = {}
        for m,n in _f_funcfg.items():
            for k,v in _cp_funcfg_dict.items():
                if k == m:
                    if _insert_type == 'group':
                        n.update({_insert_type:v})
                    elif _insert_type != 'group':
                        n.update(v)
            else:
                _funcfg.update({m:n})
        else:
            with open(Config.path_funcfg, mode='w', encoding="utf-8") as f:
                json.dump(
                    _funcfg, f, sort_keys=True,
                    indent=4, separators=(',', ':'),
                    ensure_ascii=False,
                )


