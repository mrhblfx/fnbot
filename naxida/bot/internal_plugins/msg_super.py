
from ..config import Config as Config
from ..plugin import Plugin as Plugin
from ..insert import Insert as Insert
from ..manual import Manual as Manual
from ..receive import Receive as Receive
from ..send import Send as Send

__all__ = "_msg_super",

def _msg_super(rev:dict):
    rev_msg:str = rev.get('message', '')
    if  rev_msg!= '':
        msg_type = rev['message_type'] if 'message_type' in rev else ''
        num_type:str = str(rev['user_id']) if msg_type == 'private' else str(rev['group_id'])

        if rev_msg == '/naxida':
            msg = Config.cfg_info
            Send(rev).send_msg(msg_type,num_type,msg)

        elif rev_msg == '/pluginfo':
            _info = Plugin.look_inserted_plugins()
            msg = ''
            if _info != {}:
                info = [i for i in _info.keys()]
                for i in info:
                    msg += str(i) + "\n"
                else:
                    msg = msg.rstrip("\n")
            Send(rev).send_msg(msg_type,num_type,msg)

        elif rev_msg.startswith("//fs"):
            _ = rev_msg.lstrip("//fs").lstrip()
            msg = eval(_)
            Send(rev).send_msg(msg_type,num_type,msg)

        elif rev_msg.startswith("//"):
            _ = rev_msg.lstrip("//")
            _list = _.split("\n")
            for _ in _list:
                eval(_)

        elif rev_msg.startswith("/fs"):
            msg = rev_msg.lstrip("/fs")
            Send(rev).send_msg(msg_type,num_type,msg)


