import asyncio

from fnbot import IstNotice
from fnbot import schedule
from fnbot import ciallo
from fnbot import Send

@IstNotice.manage()
@ciallo.grace()
async def _(msg_type:str, num_type:str, rev:'ciallo'):
    if rev.notice_type == "group_recall":
        if rev.operator_id != rev.self_id:
            recall_rev = Send(rev).get_msg(rev.msg_id)['data']
            recall_rev = ciallo(recall_rev)
            recall_msg = recall_rev.msg

            msg = f"[CQ:poke,qq={recall_rev.sender_user_id}]"
            Send(rev).send_msg(msg_type,num_type,msg)

            msg = recall_msg
            msg_id = Send(rev).send_msg(msg_type,num_type,msg)

            @schedule
            async def task():
                await asyncio.sleep(1)
                Send(rev).delete_msg(msg_id)
                await task.cancel()
            await task.start(rev)
