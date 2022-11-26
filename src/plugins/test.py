impor time

from fnbot import Rev
from fnbot import Send
from fnbot import IstMsg

@IstMsg.manage()
@Rev.grace('/test')
async def _(msg_type:str, num_type:str, rev:'Rev'):
    if rev.match(['ciallo', 'こんにちは', '你好']):
        msg = 'ciallo!'
        Send(rev).send_msg(msg_type, num_type, msg)
        
        
      
