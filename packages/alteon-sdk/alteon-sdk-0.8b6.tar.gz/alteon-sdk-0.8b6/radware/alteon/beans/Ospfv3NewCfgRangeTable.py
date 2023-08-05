
from radware.sdk.beans_common import *


class EnumOspfv3RangeHideState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumOspfv3RangeState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumOspfv3RangeDelete(BaseBeanEnum):
    other = 1
    delete = 2


class Ospfv3NewCfgRangeTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Addr = kwargs.get('Addr', None)
        self.Prefix = kwargs.get('Prefix', None)
        self.AreaIndex = kwargs.get('AreaIndex', None)
        self.HideState = EnumOspfv3RangeHideState.enum(kwargs.get('HideState', None))
        self.State = EnumOspfv3RangeState.enum(kwargs.get('State', None))
        self.Delete = EnumOspfv3RangeDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

