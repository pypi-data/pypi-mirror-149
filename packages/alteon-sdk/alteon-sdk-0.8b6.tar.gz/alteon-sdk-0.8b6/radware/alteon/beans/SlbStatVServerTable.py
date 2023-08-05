
from radware.sdk.beans_common import *


class SlbStatVServerTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.CurrSessions = kwargs.get('CurrSessions', None)
        self.TotalSessions = kwargs.get('TotalSessions', None)
        self.HighestSessions = kwargs.get('HighestSessions', None)
        self.HCOctetsLow32 = kwargs.get('HCOctetsLow32', None)
        self.HCOctetsHigh32 = kwargs.get('HCOctetsHigh32', None)
        self.HeaderHits = kwargs.get('HeaderHits', None)
        self.HeaderMisses = kwargs.get('HeaderMisses', None)
        self.HeaderTotalSessions = kwargs.get('HeaderTotalSessions', None)
        self.CookieRewrites = kwargs.get('CookieRewrites', None)
        self.CookieInserts = kwargs.get('CookieInserts', None)
        self.HCOctets = kwargs.get('HCOctets', None)
        self.IpAddress = kwargs.get('IpAddress', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

