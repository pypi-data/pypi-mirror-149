
from radware.sdk.beans_common import *


class AgAccessUserEnhRealsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.RealIndex = kwargs.get('RealIndex', None)

    def get_indexes(self):
        return self.Index, self.RealIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'Index', 'RealIndex',

