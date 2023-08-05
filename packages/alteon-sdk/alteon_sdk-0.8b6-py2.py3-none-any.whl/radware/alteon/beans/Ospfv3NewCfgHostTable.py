
from radware.sdk.beans_common import *


class EnumOspfv3HostState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumOspfv3HostDelete(BaseBeanEnum):
    other = 1
    delete = 2


class Ospfv3NewCfgHostTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Ip6Addr = kwargs.get('Ip6Addr', None)
        self.AreaIndex = kwargs.get('AreaIndex', None)
        self.Cost = kwargs.get('Cost', None)
        self.State = EnumOspfv3HostState.enum(kwargs.get('State', None))
        self.Delete = EnumOspfv3HostDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

