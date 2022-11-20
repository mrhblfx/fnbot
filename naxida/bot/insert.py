from typing import overload

from .config import *

__all__ = (
    "Insert",
    "InsertMessage",
    "InsertIni", "InsertSuper", "InsertPrivate",
    "InsertGroup", "InsertNotice", "InsertRequest",
    "IstMsg",
    "IstIni", "IstSuper", "IstPrivate",
    "IstGroup", "IstNotice", "IstRequest",
)

class insert(type):
    """
    Instance Properties:
    ```
        for self@insert(
            "InsertIni", "InsertSuper", "InsertPrivate",
            "InsertGroup", "InsertNotice", "InsertRequest",
        )
        insert_type:str
        fun_dict:dict
        fun_num_dict:dict
        fun_name_info:dict
        funcfg_dict:dict

        for self@insert("InsertMessage")
        insert_type:str

        for self@insert(
            "IstMsg",
            "IstIni", "IstSuper","IstPrivate",
            "IstGroup", "IstNotice", "IstRequest",
        )
        None
    ```
    """
    def __new__(cls, _name:str, _bases:tuple, _dict:dict):
        return type.__new__(cls, _name, _bases, _dict)

    def __init__(self, _name:str, _bases:tuple, _dict:dict):
        if _name in [
            "InsertIni", "InsertSuper", "InsertPrivate",
            "InsertGroup", "InsertNotice", "InsertRequest",
        ]:
            self.fun_dict = {}
            self.fun_num_dict = {}
            self.fun_name_info = {}
            self.funcfg_dict = {}
        if _name in ['InsertIni']: self.insert_type = 'ini'
        elif _name in ['InsertSuper']: self.insert_type = 'super'
        elif _name in ['InsertMessage']: self.insert_type = 'message'
        elif _name in ['InsertPrivate']: self.insert_type = 'private'
        elif _name in ['InsertGroup']: self.insert_type = 'group'
        elif _name in ['InsertNotice']: self.insert_type = 'notice'
        elif _name in ['InsertRequest']: self.insert_type = 'request'
        return type.__init__(self, _name, _bases, _dict)


class InsertIni(metaclass = insert):...
class InsertMessage(metaclass = insert):...
class InsertSuper(metaclass = insert):...
class InsertPrivate(metaclass = insert):...
class InsertGroup(metaclass = insert):...
class InsertNotice(metaclass = insert):...
class InsertRequest(metaclass = insert):...


class Insert:
    """
    Class Properties:
    ```
        insert_type:str
        fun_dict:dict
        fun_name_num:list[int]
        fun_num_dict:dict
        fun_name_info:dict
        funcfg_dict:dict
    ```
    """
    insert_type:str = "insert"
    fun_dict:dict = {}
    """for handle
    ```
    {
        fun:'function' : num:int,
        ...
    }
    ```
    """
    fun_name_num:list = [0]
    """for manage"""
    fun_num_dict:dict = {}
    """for manage
    ```
    {
        self_id:str :{
            group_id:str : {
                function:'function' : num:int,
                ...
            },
            ...
        },
        ...
    }
    or
    {
        self_id:str :{
            _insert_type:str :{
                function:'function' : num:int,
                ...
            }
        },
        ...
    }
    ```
    """
    fun_name_info:dict = {}
    """for manage
    ```
    {
        fun_name:str:{
            'function':str : fun:'function',
            'command':str : __cmd__:list,
            'num':str : num:int
        },
        ...
    }
    ```
    """
    funcfg_dict:dict = {}
    """for manage
    ```
    {
        self_id:str :{
            group_id:str:{
                fun_name:str : _bool:bool,
                ...
            },
            ...
        },
        ...
    }
    or
    {
        self_id:str :{
            _insert_type:str :{
                fun_name:str : _bool:bool,
                ...
            }
        },
        ...
    }
    ```
    """
    @overload
    @classmethod
    def handle(cls):...
    @overload
    @classmethod
    def handle(cls, _num:int, /):...
    @overload
    @classmethod
    def handle(cls, _num:int = 0):...

    @classmethod
    def handle(cls, _num:int = 0):
        """Decorate a function and add it to the main program

        Args:
        ```
            num:int (Default:>=0)   :the message triggering priority
        ```

        Raises:
        ```
            AssertionError
        ```
        """
        def decorator(f):
            assert getattr(f.__code__, 'co_flags', 0) in [147, 195]
            assert type(_num) == int
            if cls.insert_type != 'message':
                cls.fun_dict.update({f:_num})
            else:
                InsertPrivate.fun_dict.update({f:_num})
                InsertGroup.fun_dict.update({f:_num})
            return f
        return decorator


    @overload
    @classmethod
    def manage(cls):...
    @overload
    @classmethod
    def manage(cls, _dev:list, /):...
    @overload
    @classmethod
    def manage(cls, _dev:list, _group:list, /):...
    @overload
    @classmethod
    def manage(cls, _dev:list, *, _bool:bool):...
    @overload
    @classmethod
    def manage(cls, _dev:list, _group:list, _bool:bool, /):...
    @overload
    @classmethod
    def manage(cls,
        _dev:list = [], _group:list = [], _bool:bool = True, _num:int = 0,
    ):...

    @classmethod
    def manage(cls,
        _dev:list = [], _group:list = [], _bool:bool = True, _num:int = 0,
    ):
        """Decorate a function and add it to the main program

        Args:
        ```
            _bool:bool   :Default execution
            _group:list[int | str]   :The group number you want to add
            _num:int (Default:>=0)   :the message triggering priority
            _dev:list[int | str]   :The device number you want to add
        ```

        Raises:
        ```
            AssertionError
        ```
        """
        def decorator(f):
            assert getattr(f.__code__, 'co_flags', 0) in [147, 195]
            assert type(_bool) == bool
            assert type(_group) == list
            assert type(_num) == int
            assert type(_dev) == list

            if '__nickname__' in f.__dict__:
                fun_name = f.__nickname__
            elif '__nickname__' not in f.__dict__:
                _nm:int = cls.fun_name_num[0] + 1
                cls.fun_name_num.clear()
                cls.fun_name_num.append(_nm)
                fun_name = '/' + str(_nm)
            fun_cmd:list = getattr(f, '__cmd__', [])

            # Renew self.fun_name_info@insert
            assert fun_name not in cls.fun_name_info
            if cls.insert_type != 'message':
                cls.fun_name_info.update({
                    fun_name:{
                        'function':f,
                        'command':fun_cmd,
                        'num':_num,
                    }
                })
            else:
                InsertPrivate.fun_name_info.update({
                    fun_name:{
                        'function':f,
                        'command':fun_cmd,
                        'num':_num,
                    }
                })
                InsertGroup.fun_name_info.update({
                    fun_name:{
                        'function':f,
                        'command':fun_cmd,
                        'num':_num,
                    }
                })
            # Renew self.funcfg_dict@insert
            dev_list:list = []
            if _dev == []:
                for dev_ in list(Config.config_info.keys()):
                    dev_list.append(dev_)
            else:
                for dev_ in _dev:
                    if str(dev_) in list(Config.config_info.keys()):
                        dev_list.append(dev_)

            for dev_ in dev_list:
                if cls.insert_type in ['message', 'group']:
                    _ist = InsertGroup
                    if _group == []:
                        for _id in Config(dev_).group_list:
                            dict_ = _ist.funcfg_dict.get(str(dev_), {})
                            _dict:dict = dict_.get(str(_id), {})
                            _dict.update({fun_name:_bool})
                            dict_.update({str(_id):_dict})
                            _ist.funcfg_dict.update({str(dev_):dict_})
                    else:
                        for _id in _group:
                            if int(_id) in Config(dev_).group_list:
                                dict_ = _ist.funcfg_dict.get(str(dev_), {})
                                _dict:dict = dict_.get(str(_id),{})
                                _dict.update({fun_name:_bool})
                                dict_.update({str(_id):_dict})
                                _ist.funcfg_dict.update({str(dev_):dict_})
                if cls.insert_type in [
                    'insert', 'message', 'private',
                    'ini', 'super', 'notice', 'request',
                ]:
                    if cls.insert_type in ['message', 'private']:
                        _ist = InsertPrivate
                    else:
                        _ist = cls
                    dict_ = _ist.funcfg_dict.get(str(dev_), {})
                    _dict:dict = dict_.get(_ist.insert_type, {})
                    _dict.update({fun_name:_bool})
                    dict_.update({_ist.insert_type:_dict})
                    _ist.funcfg_dict.update({str(dev_):dict_})
            return f
        return decorator



class InsertIni(Insert, InsertIni):pass
class InsertMessage(Insert, InsertMessage):pass
class InsertSuper(Insert, InsertSuper):pass
class InsertPrivate(Insert, InsertPrivate):pass
class InsertGroup(Insert, InsertGroup):pass
class InsertNotice(Insert, InsertNotice):pass
class InsertRequest(Insert, InsertRequest):pass

class IstIni(InsertIni):...
class IstMsg(InsertMessage):...
class IstSuper(InsertSuper):...
class IstPrivate(InsertPrivate):...
class IstGroup(InsertGroup):...
class IstNotice(InsertNotice):...
class IstRequest(InsertRequest):...


