import requests

from .receive import *
from .config import *

__all__ = "Send",

class Send():
    """
    Args:
    ```
        self_id:dict | int | str
    ```

    Instance Properties:
    ```
        self_id:str
        host:str
        port:int
    ```

    Raises:
    ```
        TypeError
    ```
    """
    __slots__ = ('self_id', 'host', 'port',)
    host:str
    port:int

    def __init__(self, self_id):
        if type(self_id) == dict:
            self.self_id = str(self_id.get('self_id', 0))
        elif type(self_id) == int:
            self.self_id = str(self_id)
        elif type(self_id) == str:
            self.self_id = self_id
        else:
            raise TypeError("Be careful!")

        self.host = Config(self_id).host
        self.port = Config(self_id).port


    @classmethod
    def _send_msg(
        cls,
        msg_type:str, num_type:str, msg:str,
        host:str, port:int
    ):
        """Send a msssage

        Args:
        ```
            msg_type:str : Reply type (group chat/private chat)
            num_type:str | int : Reply to account number (group number/friend number)
            msg:str : Message to reply
            group_id:str | int : The group number to initiate a temporary session in the group chat
        ```
        Returns:
        ```
            msg_id:int | None
        ```
        """
        url = f"http://{host}:{port}/send_msg"
        if msg_type == "private":
            data = {
                'message_type':msg_type,
                'user_id':int(num_type),
                'message':msg
            }
            rps = requests.post(url,data)
            if rps.json()["status"] == "ok":
                msg_id = rps.json()["data"]["message_id"]
            else:
                msg_id = None
            return msg_id
        elif msg_type == "group":
            data = {
                'message_type':msg_type,
                'group_id':int(num_type),
                'message':msg
            }
            rps = requests.post(url,data)
            if rps.json()["status"] == "ok":
                msg_id = rps.json()["data"]["message_id"]
            else:
                msg_id = None
            return msg_id


    def send_msg(
        self,
        msg_type:str, num_type:str, msg:str,
    ):
        """Send a msssage

        Args:
        ```
            msg_type:str : Reply type (group chat/private chat)
            num_type:str | int : Reply to account number (group number/friend number)
            msg:str : Message to reply
            group_id:str | int : The group number to initiate a temporary session in the group chat
        ```
        Returns:
        ```
            msg_id:int | None
        ```
        """
        url = f"http://{self.host}:{self.port}/send_msg"
        if msg_type == "private":
            data = {
                'message_type':msg_type,
                'user_id':int(num_type),
                'message':msg
            }
            rps = requests.post(url,data)
            if rps.json()["status"] == "ok":
                msg_id = rps.json()["data"]["message_id"]
            else:
                msg_id = None
            return msg_id
        elif msg_type == "group":
            data = {
                'message_type':msg_type,
                'group_id':int(num_type),
                'message':msg
            }
            rps = requests.post(url,data)
            if rps.json()["status"] == "ok":
                msg_id = rps.json()["data"]["message_id"]
                _dict:dict = Receive.bot_msg_id.get(self.self_id,{})
                _list:list = _dict.get(str(num_type),[])
                _list.append(msg_id)
                _dict.update({str(num_type):_list})
                Receive.bot_msg_id.update({self.self_id:_dict})
            else:
                msg_id = None
            return msg_id


    def delete_msg(self, msg_id:int):
        """Withdraw a message

        Args:
        ```
            msg_id:int : ID of the message
        ```
        """
        data = {
            'message_id':msg_id
        }
        url = f"http://{self.host}:{self.port}/delete_msg"
        rps = requests.post(url,data)
        return rps.json()


    def get_status(self) -> dict:
        """get_status"""
        url = f"http://{self.host}:{self.port}/get_status"
        rps = requests.post(url)
        return rps.json()


    def group_ban(self,
        qq:str, group_id:str,
        time:int = 600,
    ):
        """Group single banning

        Args:
        ```
            qq:str | int : The banned qq number
            group_id:str | int : The group number where the banned qq number is located
            time:int : Ban time
        ```
        """
        data = {
            'group_id':int(group_id),
            'user_id':int(qq),
            'duration':f'{str(time)}'
        }
        url = f"http://{self.host}:{self.port}/set_group_ban"
        requests.post(url,data)


    def get_friend_list(self) -> dict:
        """Get a list of friends

        Returns:
        ```
            dict
        ```
        """
        url = f"http://{self.host}:{self.port}/get_friend_list"
        rps = requests.post(url)
        return rps.json()


    def get_group_list(self) -> dict:
        """Get a list of groups

        Returns:
        ```
            dict
        ```
        """
        url = f"http://{self.host}:{self.port}/get_group_list"
        rps = requests.post(url)
        return rps.json()


    def get_group_member_list(self, group_id:str) -> dict:
        """Get the list of group members

        Returns:
        ```
            dict
        ```
        """
        data = {
            'group_id':int(group_id)
        }
        url = f"http://{self.host}:{self.port}/get_group_member_list"
        rps = requests.post(url,data)
        return rps.json()


    def get_stranger_info(self, qq:str) -> dict:
        """Get information from strangers

        Returns:
        ```
            dict
        ```
        """
        data = {
            'user_id':int(qq)
        }
        url = f"http://{self.host}:{self.port}/get_stranger_info"
        rps = requests.post(url,data)
        return rps.json()


    def get_group_info(self, group_id:str) -> dict:
        """Get group information

        Returns:
        ```
            dict
        ```

        Others:
            `https://p.qlogo.cn/gh/{group_id}/{group_id}/100`
        """
        data = {
            'group_id':int(group_id)
        }
        url = f"http://{self.host}:{self.port}/get_group_info"
        rps = requests.post(url,data)
        return rps.json()


    def get_group_member_info(self, group_id:str, qq:str) -> dict:
        """Get group member information

        Returns:
        ```
            dict
        ```
        """
        data = {
            'group_id':int(group_id),
            'user_id':int(qq)
        }
        url = f"http://{self.host}:{self.port}/get_group_member_info"
        rps = requests.post(url,data)
        return rps.json()


    def get_msg(self, message_id:str) -> dict:
        """Get message

        Returns:
        ```
            dict
        ```
        """
        data = {
            'message_id':int(message_id)
        }
        url = f"http://{self.host}:{self.port}/get_msg"
        rps = requests.post(url,data)
        return rps.json()


