
from radware.sdk.beans_common import *


class EnumIfClearStats(BaseBeanEnum):
    ok = 1
    clear = 2


class IfStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.ClearStats = EnumIfClearStats.enum(kwargs.get('ClearStats', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

