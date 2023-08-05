
from radware.sdk.beans_common import *


class SlbStatGroupTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.CurrSessions = kwargs.get('CurrSessions', None)
        self.TotalSessions = kwargs.get('TotalSessions', None)
        self.HighestSessions = kwargs.get('HighestSessions', None)
        self.HCOctetsLow32 = kwargs.get('HCOctetsLow32', None)
        self.HCOctetsHigh32 = kwargs.get('HCOctetsHigh32', None)
        self.HCOctets = kwargs.get('HCOctets', None)
        self.WlmUpdates = kwargs.get('WlmUpdates', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

