
from radware.sdk.beans_common import *


class SlbSessionInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.SpIndex = kwargs.get('SpIndex', None)
        self.Index = kwargs.get('Index', None)
        self.String = kwargs.get('String', None)

    def get_indexes(self):
        return self.SpIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'SpIndex', 'Index',

