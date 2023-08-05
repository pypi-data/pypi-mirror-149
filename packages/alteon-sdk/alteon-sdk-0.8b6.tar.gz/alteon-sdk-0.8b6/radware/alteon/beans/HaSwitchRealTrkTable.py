
from radware.sdk.beans_common import *


class HaSwitchRealTrkTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

