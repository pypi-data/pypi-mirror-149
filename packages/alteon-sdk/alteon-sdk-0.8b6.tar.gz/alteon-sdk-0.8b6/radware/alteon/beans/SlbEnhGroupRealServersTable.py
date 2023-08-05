
from radware.sdk.beans_common import *


class SlbEnhGroupRealServersTable(DeviceBean):
    def __init__(self, **kwargs):
        self.RealServerGroupIndex = kwargs.get('RealServerGroupIndex', None)
        self.Index = kwargs.get('Index', None)

    def get_indexes(self):
        return self.RealServerGroupIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'RealServerGroupIndex', 'Index',

