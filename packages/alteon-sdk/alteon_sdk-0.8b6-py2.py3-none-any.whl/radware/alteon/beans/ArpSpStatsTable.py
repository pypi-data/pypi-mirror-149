
from radware.sdk.beans_common import *


class ArpSpStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.SpIndex = kwargs.get('SpIndex', None)
        self.Entries = kwargs.get('Entries', None)
        self.HighWater = kwargs.get('HighWater', None)
        self.MaxEntries = kwargs.get('MaxEntries', None)

    def get_indexes(self):
        return self.SpIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'SpIndex',

