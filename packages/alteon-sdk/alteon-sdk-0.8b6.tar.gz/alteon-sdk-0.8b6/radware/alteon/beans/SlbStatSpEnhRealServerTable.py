
from radware.sdk.beans_common import *


class SlbStatSpEnhRealServerTable(DeviceBean):
    def __init__(self, **kwargs):
        self.SpIndex = kwargs.get('SpIndex', None)
        self.ServerIndex = kwargs.get('ServerIndex', None)
        self.CurrSessions = kwargs.get('CurrSessions', None)
        self.TotalSessions = kwargs.get('TotalSessions', None)
        self.HCOctetsLow32 = kwargs.get('HCOctetsLow32', None)
        self.HCOctetsHigh32 = kwargs.get('HCOctetsHigh32', None)
        self.HCOctets = kwargs.get('HCOctets', None)

    def get_indexes(self):
        return self.SpIndex, self.ServerIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'SpIndex', 'ServerIndex',

