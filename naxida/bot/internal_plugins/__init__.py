r"""Just a built-in plug-in, but essential"""

from ..insert import (
    InsertSuper,
)

from .msg_super import *

@InsertSuper.handle()
def _(rev:dict):
    _msg_super(rev)


