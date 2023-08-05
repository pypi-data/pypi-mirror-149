
from radware.sdk.beans_common import *


class EnumOspfHostState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumOspfHostDelete(BaseBeanEnum):
    other = 1
    delete = 2


class OspfNewCfgHostTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.IpAddr = kwargs.get('IpAddr', None)
        self.AreaIndex = kwargs.get('AreaIndex', None)
        self.Cost = kwargs.get('Cost', None)
        self.State = EnumOspfHostState.enum(kwargs.get('State', None))
        self.Delete = EnumOspfHostDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

