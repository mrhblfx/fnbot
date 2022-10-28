import os
import sys
import toml

__all__ = 'Config',

def _cfg(objcls, fp_pybot:str, config_dict:dict):
    """
    Args:
    ```
        objcls:'Config'
        fp_pybot:str
        config_dict:dict :Single number
    ```

    Returns:
    ```
        objcls:'Config'
    ```
    """
    path_pybot:str = fp_pybot
    path_funcfg:str = fp_pybot + "/funcfg.json"
    path_plugins:str = fp_pybot + "/src/plugins"
    host:str = config_dict['host'] if 'host' in config_dict else ''
    port:int = config_dict['port'] if 'port' in config_dict else 9900
    post:int = config_dict['post'] if 'post' in config_dict else 9901
    bot_qq:int = config_dict['bot_qq'] if 'bot_qq' in config_dict else 0
    group_list:list = config_dict['group_list'] if 'group_list' in config_dict else []
    nickname:str = config_dict['nickname'] if 'nickname' in config_dict else ''
    super_qq:int = config_dict['super_qq'] if 'super_qq' in config_dict else 0
    admin_list:list = config_dict['admin_list'] if 'admin_list' in config_dict else []
    blackqq_list:list = config_dict['blackqq_list'] if 'blackqq_list' in config_dict else []

    objcls.config_info.update({str(bot_qq):{
        'path_pybot':path_pybot, 'path_funcfg':path_funcfg,
        'path_plugins':path_plugins,
        'host':host, 'port':port, 'post':post,
        'bot_qq':bot_qq, 'group_list':group_list,
        'nickname':nickname, 'super_qq':super_qq,
        'admin_list':admin_list, 'blackqq_list':blackqq_list,
    }})
    return objcls


def _cfgs(objcls, fp_pybot:str, config_dict:dict):
    """
    Args:
    ```
        objcls:'Config'
        fp_pybot:str
        config_dict:dict : Multiple number, or {}
    ```

    Returns:
    ```
        objcls:'Config'
    ```
    """
    if config_dict == {}:
        return _cfg(objcls, fp_pybot, config_dict)

    _info_ = {}
    for k,v in config_dict.items():
        k:str ; v:dict

        path_pybot:str = fp_pybot
        path_funcfg:str = fp_pybot + "/funcfg.json"
        path_plugins:str = fp_pybot + "/src/plugins"
        host:str = v['host'] if 'host' in v else ''
        port:int = v['port'] if 'port' in v else 9900
        post:int = v['post'] if 'post' in v else 9901
        bot_qq:int = v['bot_qq'] if 'bot_qq' in v else 0
        group_list:list = v['group_list'] if 'group_list' in v else []
        nickname:str = v['nickname'] if 'nickname' in v else ''
        super_qq:int = v['super_qq'] if 'super_qq' in v else 0
        admin_list:list = v['admin_list'] if 'admin_list' in v else []
        blackqq_list:list = v['blackqq_list'] if 'blackqq_list' in v else []

        _info_.update({str(bot_qq):{
            'path_pybot':path_pybot, 'path_funcfg':path_funcfg,
            'path_plugins':path_plugins,
            'host':host, 'port':port, 'post':post,
            'bot_qq':bot_qq, 'group_list':group_list,
            'nickname':nickname, 'super_qq':super_qq,
            'admin_list':admin_list, 'blackqq_list':blackqq_list,
        }})
    else:
        objcls.config_info.update(_info_)
    return objcls


def _config(objcls):
    """
    Args:
    ```
        objcls:'Config'
    ```

    Returns:
    ```
        function() -> objcls:'Config'
    ```
    """
    os.chdir(sys.path[0])
    fp:str = os.getcwd()
    fp_pybot:str = eval(repr(fp).replace('\\\\','/'))
    if fp_pybot[1] == ":":
        _,__ = fp_pybot.split(":")
        fp_pybot = _.upper() + ":" + __
    fp = fp_pybot + "/pybot.toml"

    objcls.path_pybot = fp_pybot
    objcls.path_funcfg = fp_pybot + "/funcfg.json"
    objcls.path_plugins = fp_pybot + "/src/plugins"

    if os.path.exists(fp):
        # with open(fp , mode='rb') as f:
        #     content = f.read()
        #     config_dict = toml.loads(content.decode('utf8'))
        with open(fp, mode='r', encoding="utf-8") as f:
            config_dict = toml.load(f)
        _config_dict = {}
        if all((
            'host' in config_dict, type(config_dict.get('host')) == str,
            'port' in config_dict, type(config_dict.get('port')) == int,
            'post' in config_dict, type(config_dict.get('post')) == int,
            'bot_qq' in config_dict, type(config_dict.get('bot_qq')) == int,
            'group_list' in config_dict, type(config_dict.get('group_list')) == list,
        )):
            _config_dict.update({str(config_dict.get('bot_qq')):config_dict})
            return _cfg(objcls, fp_pybot, _config_dict)
        else:
            for k,v in config_dict.items():
                if type(v) == dict:
                    v:dict
                    if all((
                        'host' in v, type(v.get('host')) == str,
                        'port' in v, type(v.get('port')) == int,
                        'post' in v, type(v.get('post')) == int,
                        'bot_qq' in v, type(v.get('bot_qq')) == int,
                        'group_list' in v, type(v.get('group_list')) == list,
                    )):
                        _config_dict.update(({k:v}))
            else:
                return _cfgs(objcls, fp_pybot, _config_dict)
    else:
        _config_dict = {
            'host': '127.0.0.1',
            'port': 9900,
            'post': 9901,
            'bot_qq': 0,
            'group_list': [],
            'nickname': '',
            'super_qq': 0,
            'admin_list':[],
            'blackqq_list':[],
        }
        return _cfg(objcls, fp_pybot, _config_dict)


class CfgInfo():
    def __init__(self, f):...

    def __get__(self, objself, objcls):
        return objcls.__str__(objcls)


class Info():
    """A descriptor, in order to add the attribute `info` to `Config`

    If the class being used is instantiated, then:

    `objself:instantiated object, objcls:class object`

    If not, then:

    `objself:None, objcls:class object`
    """
    def __get__(self, objself, objcls):
        return objcls.__str__(objcls)


@_config
class Config():
    """
    Args:
    ```
        self_id:dict | int | str
    ```

    Class Properties:
    ```
        info:str
        config_info:dict
        path_pybot:str
        path_funcfg:str
        path_plugins:str
    ```

    Instance Properties:
    ```
        self_id:str
        host:str # Must be present in the configuration file
        port:int # Must be present in the configuration file
        post:int # Must be present in the configuration file
        bot_qq:int # Must be present in the configuration file
        group_list:list[int] # Must be present in the configuration file
        nickname:str
        super_qq:int
        admin_list:list[int]
        blackqq_list:list[int]
    ```

    Raises:
    ```
        TypeError
    ```
    """
    __slots__ = (
        'self_id',
        'host', 'port', 'post', 'bot_qq', 'group_list',
        'nickname', 'super_qq', 'admin_list', 'blackqq_list',
    )
    info = Info()
    """Returns all configuration information
    (based on the file `pybot.toml`)
    """
    config_info:dict = {}
    """Contains all configuration information
    (based on the file `pybot.toml`)
    * `dict[str:dict]`
    """

    path_pybot:str
    path_funcfg:str
    path_plugins:str
    host:str
    port:int
    post:int
    bot_qq:int
    group_list:list
    """`list[int]`"""
    nickname:str
    super_qq:int
    admin_list:list
    """`list[int]`"""
    blackqq_list:list
    """`list[int]`"""

    def __init__(self, self_id):
        if type(self_id) == dict:
            self.self_id = str(self_id.get('self_id', 0))
        elif type(self_id) == int:
            self.self_id = str(self_id)
        elif type(self_id) == str:
            self.self_id = self_id
        else:
            raise TypeError("Be careful!")

        _config_dict:dict = self.config_info.get(self.self_id)
        self.host = _config_dict['host']
        self.port = _config_dict['port']
        self.post = _config_dict['post']
        self.bot_qq = _config_dict['bot_qq']
        self.nickname = _config_dict['nickname']
        self.super_qq = _config_dict['super_qq']
        self.admin_list:list = _config_dict['admin_list']
        self.blackqq_list:list = _config_dict['blackqq_list']
        self.group_list:list = _config_dict['group_list']


    def __str__(self) -> str:
        """Returns all configuration information
        (based on the file `pybot.toml`)
        """
        _str = ''
        for k,v in self.config_info.items():
            _str += k + "\n"
            _str += 'path_pybot:' + str(v['path_pybot']) + "\n"
            _str += 'path_funcfg:' + str(v['path_funcfg']) + "\n"
            _str += 'path_plugins:' + str(v['path_plugins']) + "\n"
            _str += 'host:' + str(v['host']) + "\n"
            _str += 'port:' + str(v['port']) + "\n"
            _str += 'post:' + str(v['post']) + "\n"
            _str += 'bot_qq:' + str(v['bot_qq']) + "\n"
            _str += 'group_list:' + str(v['group_list']) + "\n"
            _str += 'nickname:' + str(v['nickname']) + "\n"
            _str += 'super_qq:' + str(v['super_qq']) + "\n"
            _str += 'admin_list:' + str(v['admin_list']) + "\n"
            _str += 'blackqq_list:' + str(v['blackqq_list']) + "\n"
            _str += "\n"
        else:
            _str = _str.rstrip("\n").rstrip("\n")
        return _str


    @classmethod
    def __call__(cls):
        """Returns all configuration information
        (based on the file `pybot.toml`)
        """
        return cls.__str__(cls)


    @CfgInfo
    def cfg_info(self):
        """Contains all configuration information
        (based on the file `pybot.toml`)
        """
        pass


    @classmethod
    def cfginfo(cls) -> str:
        """Returns all configuration information
        (based on the file `pybot.toml`)
        """
        return cls.__str__(cls)


    @classmethod
    def renewal(cls):
        """Update all configuration information"""
        _config(cls)


