from abc import ABCMeta, abstractmethod
from typing import Union


class Module(metaclass=ABCMeta):
    @abstractmethod
    def GetHeaderValue(self, type: int) -> Union[int, str, float]:
        pass
    @abstractmethod
    def SetInputValue(self, type: int, code: str):
        pass
    @abstractmethod
    def Subscribe(self):
        pass
    @abstractmethod
    def Unsubscribe(self):
        pass