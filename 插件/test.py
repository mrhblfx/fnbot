import time
import asyncio

from fnbot import IstMsg
from fnbot import ciallo
from fnbot import Send
from fnbot import schedule

@IstMsg.manage()
@ciallo.grace()
async def _(msg_type:str, num_type:str, rev:ciallo):
    if rev.match(["riddle",]):
        issue = (
            'Is it reasonable to '
            'treat the Me3Si group as if it were a big proton '
            'in some circumstances?'
        )
        answer = ['Yes', 'yes']
        now_time = time.strftime("%Y-%m-%d %H:%M:%S")
        msg = (
            f"[CQ:reply,id={rev.msg_id}]"
            f"[CQ:at,qq={str(rev.qq)}]"
            f"[CQ:at,qq={str(rev.qq)}]\n\n"
            f"{issue}\n\n"
            f"{now_time}"
        )
        msg = ciallo.compat_msg(msg, msg_type, rev)
        Send(rev).send_msg(msg_type, num_type, msg)

        frequency:int = 0
        @schedule
        async def task():
            nonlocal frequency
            while True:
                frequency += 1
                _rev = await rev.awtrev()
                if all((
                    _rev.msg == 'answer', _rev.identify_privilege(True),
                )):
                    msg = (
                        f"The answer is as follows:\n\n"
                        f"Yes or yes"
                    )
                    Send(rev).send_msg(msg_type, num_type, msg)
                    frequency -= 1
                elif _rev.msg in answer:
                    msg=(
                        f"[CQ:at,qq={rev.qq}]\n"
                        f"Congratulation on your correct answer!"
                    )
                    msg = ciallo.compat_msg(msg, msg_type, rev)
                    Send(rev).send_msg(msg_type, num_type, msg)
                    await task.cancel()
                elif frequency == 3:
                    msg = (
                        f"[CQ:at,qq={str(rev.qq)}]\n"
                        f"The maximum number of answers has been reached!\n"
                        f"The answer is as follows:\n\n"
                        f"Yes or yes"
                    )
                    msg = ciallo.compat_msg(msg, msg_type, rev)
                    Send(rev).send_msg(msg_type, num_type, msg)
                    await task.cancel()
                else:
                    msg=(
                        f"[CQ:at,qq={str(rev.qq)}]\n"
                        f"The answer doesn't seem to be this!"
                    )
                    msg = ciallo.compat_msg(msg, msg_type, rev)
                    Send(rev).send_msg(msg_type, num_type, msg)

        @task.awtwait
        async def task():
            while True:
                _rev = await rev.awtexcrev()
                if all((
                    _rev.msg == 'answer', _rev.identify_privilege(True),
                )):
                    msg = (
                        f"The answer is as follows:\n\n"
                        f"Yes or yes"
                    )
                    Send(rev).send_msg(msg_type, num_type, msg)

        @task.awtdecline
        async def task():
            await asyncio.sleep(180)
            msg = (
                f"[CQ:at,qq={rev.qq}]\n"
                f"Wait timeout!!!\n"
                f"The answer is as follows:\n\n"
                f"Yes or yes"
            )
            msg = ciallo.compat_msg(msg, msg_type, rev)
            Send(rev).send_msg(msg_type, num_type, msg)
            await task.cancel()
        await task.start(rev)
