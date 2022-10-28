

from .config import *

__all__ = (
    "InsertIni", "InsertOthers", "InsertSuper",
    "InsertPrivate", "InsertGroup", "InsertNotice", "InsertRequest",
    "IstIni", "IstOthers", "IstSuper",
    "IstPrivate", "IstGroup", "IstNotice", "IstRequest",
)

class Insert(type):
    """
    Class Properties:
    ```
        fun_name_num:list[int]
        fun_dict:dict
        fun_num_dict:dict
        fun_name_info:dict
        funcfg_dict:dict
    ```

    Instance Properties:
    ```
        insert_type:str
        fun_dict:dict
        fun_num_dict:dict
        fun_name_info:dict
        funcfg_dict:dict
    ```
    """
    fun_dict:dict
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
    fun_num_dict:dict
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
    fun_name_info:dict
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
    funcfg_dict:dict
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
    def __new__(cls, _name:str, _bases:tuple, _dict:dict):
        return type.__new__(cls, _name, _bases, _dict)


    def __init__(self, _name:str, _bases:tuple, _dict:dict):
        self.fun_dict = {}
        self.fun_num_dict = {}
        self.fun_name_info = {}
        self.funcfg_dict = {}
        # self.handle = classmethod(self.handle)
        # self.manage = classmethod(self.manage)
        if _name in ['InsertIni']:
            self.insert_type = 'ini'
        elif _name in ['InsertOthers']:
            self.insert_type = 'others'
        elif _name in ['InsertSuper']:
            self.insert_type = 'super'
        elif _name in ['InsertPrivate']:
            self.insert_type = 'private'
        elif _name in ['InsertGroup']:
            self.insert_type = 'group'
        elif _name in ['InsertNotice']:
            self.insert_type = 'notice'
        elif _name in ['InsertRequest']:
            self.insert_type = 'request'
        return type.__init__(self, _name, _bases, _dict)


    def handle(self, num:int = 0):
        """Decorate a function and add it to the main program

        Args:
        ```
            num:int (Default:>=0) : the message triggering priority
        ```

        Returns:
        ```
            decorator:'function'
            decorator(f:'function') -> f:'function'
        ```

        Usage:
        ```
            @InsertXxx.handle()
            def _():...
        ```
        """
        def decorator(f:'function'):
            self.fun_dict.update({f:num})
            return f
        return decorator


    def manage(self,
        _dev:list = [], _group:list = [],
        _bool:bool = True, _num:int = 0,
    ):
        """Decorate a function and add it to the main program

        Args:
        ```
            _bool:bool :Default execution
            _group:list[int | str] :The group number you want to add
            _num:int (Default:>=0) :the message triggering priority
            _dev:list[int | str] :The device number you want to add
        ```

        Returns:
        ```
            decorator:'function'
            decorator(f:'function') -> f:'function'
        ```

        Usage:
        ```
            @InsertXxx.manage()
            def _():...
        ```
        """
        def decorator(f:'function'):
            if type(_bool) != bool:
                raise TypeError("_bool should be bool!")
            if type(_group) != list:
                raise TypeError("_group should be list!")
            if type(_num) != int:
                raise TypeError("_num should be int!")
            if type(_dev) != list:
                raise TypeError("_dev should be list!")

            if '__nickname__' in f.__dict__:
                fun_name = f.__nickname__
            elif '__nickname__' not in f.__dict__:
                _nm:int = self.fun_name_num[0] + 1
                self.fun_name_num.clear()
                self.fun_name_num.append(_nm)
                fun_name = '/' + str(_nm)
            fun_cmd:list = f.__cmd__ if '__cmd__' in f.__dict__ else []

            # Renew self.fun_name_info
            if fun_name in self.fun_name_info:
                raise RuntimeError("The fun_name already exists!")
            else:
                self.fun_name_info.update({
                    fun_name:{
                        'function':f,
                        'command':fun_cmd,
                        'num':_num,
                    }
                })
            # Renew self.funcfg_dict
            dev_list:list = []
            if _dev == []:
                for dev_ in list(Config.config_info.keys()):
                    dev_list.append(dev_)
            else:
                for dev_ in _dev:
                    if str(dev_) in list(Config.config_info.keys()):
                        dev_list.append(dev_)

            for dev_ in dev_list:
                if self.insert_type == 'group':
                    if _group == []:
                        for _id in Config(dev_).group_list:
                            dict_ = self.funcfg_dict.get(str(dev_),{})
                            _dict:dict = dict_.get(str(_id),{})
                            _dict.update({fun_name:_bool})
                            dict_.update({str(_id):_dict})
                            self.funcfg_dict.update({str(dev_):dict_})
                    else:
                        for _id in _group:
                            if int(_id) in Config(dev_).group_list:
                                dict_ = self.funcfg_dict.get(str(dev_),{})
                                _dict:dict = dict_.get(str(_id),{})
                                _dict.update({fun_name:_bool})
                                dict_.update({str(_id):_dict})
                                self.funcfg_dict.update({str(dev_):dict_})
                elif self.insert_type in [
                    'private', 'notice', 'request',
                    'ini', 'others', 'super',
                ]:
                    dict_ = self.funcfg_dict.get(str(dev_),{})
                    _dict:dict = dict_.get(self.insert_type,{})
                    _dict.update({fun_name:_bool})
                    dict_.update({self.insert_type:_dict})
                    self.funcfg_dict.update({str(dev_):dict_})
            return f
        return decorator



class InsertIni(metaclass = Insert):pass
class InsertOthers(metaclass = Insert):pass
class InsertSuper(metaclass = Insert):pass
class InsertPrivate(metaclass = Insert):pass
class InsertGroup(metaclass = Insert):pass
class InsertNotice(metaclass = Insert):pass
class InsertRequest(metaclass = Insert):pass

class IstIni(InsertIni):...
class IstOthers(InsertOthers):...
class IstSuper(InsertSuper):...
class IstPrivate(InsertPrivate):...
class IstGroup(InsertGroup):...
class IstNotice(InsertNotice):...
class IstRequest(InsertRequest):...


