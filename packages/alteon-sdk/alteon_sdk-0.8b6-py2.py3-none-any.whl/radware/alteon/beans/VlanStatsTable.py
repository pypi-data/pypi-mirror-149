
from radware.sdk.beans_common import *


class EnumVlanStatsClear(BaseBeanEnum):
    ok = 1
    clear = 2


class VlanStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Clear = EnumVlanStatsClear.enum(kwargs.get('Clear', None))
        self.RealIndex = kwargs.get('RealIndex', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

