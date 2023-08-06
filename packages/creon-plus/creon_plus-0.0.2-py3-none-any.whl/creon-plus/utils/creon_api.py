from typing import TYPE_CHECKING, Type
from win32com.client import Dispatch, WithEvents

import constants

if TYPE_CHECKING:
    from models import Module, EventHandler

def get_stock_cur_module() -> 'Module':
    return Dispatch(constants.STOCK_CUR)

def bind_module_with_eventhandler(module: 'Module', handler: Type['EventHandler']) -> 'EventHandler':
    return WithEvents(module, handler)
