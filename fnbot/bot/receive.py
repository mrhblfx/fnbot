import json
import time
import socket

from .config import *

__all__ = "Receive",



class Receive():
    """Receiving messages from go-cqhttp and processing it

    Args:
    ```
        self_id: 'Rev' | 'Ciallo' | 'ciallo' | dict | int | str
    ```

    Class Properties:
    ```
        rev_list:list
        bot_msg_id:dict
    ```

    Instance Properties:
    ```
        self_id:str
        host:str
        post:int
        botsocket:'socket'
    ```
    """
    __slots__ = ('self_id', 'host', 'post','botsocket',)
    dev_list:list = []
    rev_list:list = []
    """`list[rev:dict]`"""
    bot_msg_id:dict = {}
    """Store message-ids(in group) sent by bot itself
    ```
    {
        self_id:str :{
            group_id:str : [msg_id:int],
            ...
        },
        ...
    }
    ```

    Raises:
    ```
        TypeError
    ```
    """
    def __init__(self, self_id):
        if any((
            # isinstance(self_id, (Rev, Ciallo, ciallo)),
            type(self_id).__name__ in ['Rev', 'Ciallo', 'ciallo'],
        )):
            self.self_id = str(getattr(self_id, 'self_id'))
        elif type(self_id) == dict:
            self.self_id = str(self_id.get('self_id'))
        elif type(self_id) == int:
            self.self_id = str(self_id)
        elif type(self_id) == str:
            self.self_id = self_id
        else:
            raise TypeError("Be careful!")

        self.dev_list.append(self)
        self.host = Config(self_id).host
        self.post = Config(self_id).post
        self.botsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def __call__(self):
        while True:
            try: self.launch()
            except:...


    def bind(self):
        _is = True
        _is_bind = True
        while _is:
            while _is_bind:
                try:
                    self.botsocket.bind((self.host, self.post))
                    self.botsocket.listen(100)
                    _is_bind = False
                except:
                    print("~~~少女祈祷中~~~")
                    time.sleep(3)
            _is = False


    def launch(self):
        header = 'HTTP/1.1 200 OK\n\n'
        conn = self.botsocket.accept()[0]
        with conn:
            data = conn.recv(16384).decode(encoding='utf-8')
            conn.sendall((header).encode(encoding='utf-8'))
            rev_json = self._request_to_json(data)

        if rev_json != None: self.rev_list.append(rev_json)

        if self.bot_msg_id != {}:
            k:str ; v:dict ; m:str ; n:list
            for k,v in self.bot_msg_id.items():
                for m,n in v.items():
                    if len(n) >= 999:
                        n.pop(0)
                        v.update({m,n})
                        self.bot_msg_id.update({k:v})


    @classmethod
    def _request_to_json(cls, msg):
        for i in range(len(msg)):
            if msg[i] == "{" and msg[-1] == "\n":
                return json.loads(msg[i:])
        return None


