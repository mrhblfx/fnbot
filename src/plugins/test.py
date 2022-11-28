from fnbot import Rev
from fnbot import Send
from fnbot import IstMsg

@IstMsg.manage()
@Rev.grace()
async def _(msg_type:str, num_type:str, rev:'Rev'):
    if rev.match(['ciallo',]):
        msg = 'ciallo!'
        Send(rev).send_msg(msg_type, num_type, msg)
