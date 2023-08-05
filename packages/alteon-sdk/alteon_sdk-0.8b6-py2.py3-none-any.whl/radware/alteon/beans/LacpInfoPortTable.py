
from radware.sdk.beans_common import *


class EnumLacpInfoPortSelected(BaseBeanEnum):
    selected = 1
    unselected = 2
    standby = 3


class EnumLacpInfoPortNtt(BaseBeanEnum):
    true = 1
    false = 2


class EnumLacpInfoPortReadyN(BaseBeanEnum):
    true = 1
    false = 2


class EnumLacpInfoPortMoved(BaseBeanEnum):
    true = 1
    false = 2


class LacpInfoPortTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Selected = EnumLacpInfoPortSelected.enum(kwargs.get('Selected', None))
        self.Ntt = EnumLacpInfoPortNtt.enum(kwargs.get('Ntt', None))
        self.ReadyN = EnumLacpInfoPortReadyN.enum(kwargs.get('ReadyN', None))
        self.Moved = EnumLacpInfoPortMoved.enum(kwargs.get('Moved', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

