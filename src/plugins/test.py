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
        
        
@IstMsg.manage()
@Rev.grace('/basic_time')
async def _(msg_type:str, num_type:str, rev:'Rev'):
    if rev.match('时间'):
        wl = "一二三四五六天"
        weekday = wl[time.localtime().tm_wday]
        now_time = time.strftime("%Y-%m-%d %H:%M:%S")
        msg=(
            f"{now_time}\t星期{weekday}"
        )
        Send(rev).send_msg(msg_type, num_type, msg)


