from dataclasses import dataclass


@dataclass
class LivePrice:
    code: str
    '''type 0'''
    name: str
    '''type 1'''
    price: int
    '''type 13 - 현재가'''
    time: int
    '''type 18 - 시간'''
