
from radware.sdk.beans_common import *


class EnumOspfRangeHideState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumOspfRangeState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumOspfRangeDelete(BaseBeanEnum):
    other = 1
    delete = 2


class OspfNewCfgRangeTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Addr = kwargs.get('Addr', None)
        self.Mask = kwargs.get('Mask', None)
        self.AreaIndex = kwargs.get('AreaIndex', None)
        self.HideState = EnumOspfRangeHideState.enum(kwargs.get('HideState', None))
        self.State = EnumOspfRangeState.enum(kwargs.get('State', None))
        self.Delete = EnumOspfRangeDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

