import json
import time
import socket

from .charming import Rev, Ciallo, ciallo
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
        ListenSocket:'socket'
    ```
    """
    __slots__ = ('self_id', 'host', 'post','ListenSocket',)
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
            isinstance(self_id, (Rev, Ciallo, ciallo)),
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
        self.ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def bind(self):
        _is = True
        _is_bind = True
        while _is:
            while _is_bind:
                try:
                    self.ListenSocket.bind((self.host, self.post))
                    self.ListenSocket.listen(100)
                    _is_bind = False
                except:
                    print("~~~少女祈祷中~~~")
                    time.sleep(3)
            _is = False


    def launch(self):
        HttpResponseHeader = 'HTTP/1.1 200 OK\n\n'
        Client, Address = self.ListenSocket.accept()
        Request = Client.recv(4096).decode(encoding='utf-8')
        rev_json = self._request_to_json(Request)
        Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))
        Client.close()

        if rev_json != None:
            rev:dict = rev_json
            self.rev_list.append(rev)

        if self.bot_msg_id != {}:
            k:str ; v:dict ; m:str ; n:list
            for k,v in self.bot_msg_id.items():
                for m,n in v.items():
                    if len(n) >1000:
                        n.pop(0)
                        v.update({m,n})
                        self.bot_msg_id.update({k:v})


    def __call__(self):
        while True:
            self.launch()


    @classmethod
    def _request_to_json(cls,msg):
        for i in range(len(msg)):
            if msg[i] == "{" and msg[-1] == "\n":
                return json.loads(msg[i:])
        return None


