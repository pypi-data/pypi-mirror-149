
from radware.sdk.beans_common import *


class HaServiceVipTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.HaServiceVipIndex = kwargs.get('HaServiceVipIndex', None)

    def get_indexes(self):
        return self.Index, self.HaServiceVipIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'Index', 'HaServiceVipIndex',

