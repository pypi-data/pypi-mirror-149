
from radware.sdk.beans_common import *


class HaServiceFipTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.FipIndex = kwargs.get('FipIndex', None)

    def get_indexes(self):
        return self.Index, self.FipIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'Index', 'FipIndex',

