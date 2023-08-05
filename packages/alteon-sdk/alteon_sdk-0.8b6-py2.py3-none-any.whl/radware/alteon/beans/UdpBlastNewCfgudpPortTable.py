
from radware.sdk.beans_common import *


class EnumUdpBlastCfgudpPortEntryDelete(BaseBeanEnum):
    other = 1
    delete = 2


class UdpBlastNewCfgudpPortTable(DeviceBean):
    def __init__(self, **kwargs):
        self.LowIndx = kwargs.get('LowIndx', None)
        self.HighIndx = kwargs.get('HighIndx', None)
        self.Delete = EnumUdpBlastCfgudpPortEntryDelete.enum(kwargs.get('Delete', None))
        self.PacketLimit = kwargs.get('PacketLimit', None)

    def get_indexes(self):
        return self.LowIndx, self.HighIndx,
    
    @classmethod
    def get_index_names(cls):
        return 'LowIndx', 'HighIndx',

