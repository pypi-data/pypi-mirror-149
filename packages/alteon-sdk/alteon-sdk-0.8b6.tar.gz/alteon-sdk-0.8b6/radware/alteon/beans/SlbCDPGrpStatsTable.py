
from radware.sdk.beans_common import *


class SlbCDPGrpStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.LastSuccess = kwargs.get('LastSuccess', None)
        self.LastFailed = kwargs.get('LastFailed', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

