from typing import TYPE_CHECKING
from models import EventHandler

if TYPE_CHECKING:
    from models import Module

class LivePriceHandler(EventHandler):
    def init(self, module: 'Module') -> None:
        self.__module = module

    def subscribe(self) -> None:
        self.__module.Subscribe()

    def unsubscribe(self) -> None:
        self.__module.Unsubscribe()

    def OnReceived(self) -> None:
        raise Exception('implement your business logic')
