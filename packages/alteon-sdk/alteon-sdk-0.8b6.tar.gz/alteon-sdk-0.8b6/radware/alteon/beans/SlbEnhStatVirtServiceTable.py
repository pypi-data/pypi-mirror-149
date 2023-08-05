
from radware.sdk.beans_common import *


class SlbEnhStatVirtServiceTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ServerIndex = kwargs.get('ServerIndex', None)
        self.Index = kwargs.get('Index', None)
        self.RealServerIndex = kwargs.get('RealServerIndex', None)
        self.CurrSessions = kwargs.get('CurrSessions', None)
        self.TotalSessions = kwargs.get('TotalSessions', None)
        self.HighestSessions = kwargs.get('HighestSessions', None)
        self.HCOctetsLow32 = kwargs.get('HCOctetsLow32', None)
        self.HCOctetsHigh32 = kwargs.get('HCOctetsHigh32', None)
        self.HCOctets = kwargs.get('HCOctets', None)
        self.RealStatus = kwargs.get('RealStatus', None)
        self.HcReason = kwargs.get('HcReason', None)
        self.RSTSessions = kwargs.get('RSTSessions', None)

    def get_indexes(self):
        return self.ServerIndex, self.Index, self.RealServerIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'ServerIndex', 'Index', 'RealServerIndex',

