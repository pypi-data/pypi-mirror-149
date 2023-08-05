
from radware.sdk.beans_common import *


class EnumAgSysPeerState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumAgSysPeerDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumAgSysPeerAddrType(BaseBeanEnum):
    ipv4 = 4
    ipv6 = 6


class AgSysPeerNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Addr = kwargs.get('Addr', None)
        self.State = EnumAgSysPeerState.enum(kwargs.get('State', None))
        self.VadcBmap = kwargs.get('VadcBmap', None)
        self.Delete = EnumAgSysPeerDelete.enum(kwargs.get('Delete', None))
        self.VadcAdd = kwargs.get('VadcAdd', None)
        self.VadcRemove = kwargs.get('VadcRemove', None)
        self.AddrType = EnumAgSysPeerAddrType.enum(kwargs.get('AddrType', None))
        self.Ipv6Addr = kwargs.get('Ipv6Addr', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

