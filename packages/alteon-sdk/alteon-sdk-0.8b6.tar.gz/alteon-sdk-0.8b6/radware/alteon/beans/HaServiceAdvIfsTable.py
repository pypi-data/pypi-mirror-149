
from radware.sdk.beans_common import *


class HaServiceAdvIfsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.AdvIfIndex = kwargs.get('AdvIfIndex', None)

    def get_indexes(self):
        return self.Index, self.AdvIfIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'Index', 'AdvIfIndex',

