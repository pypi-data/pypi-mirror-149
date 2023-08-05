
from radware.sdk.beans_common import *


class SlbStatLinkpfIpTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.UpBwCurr = kwargs.get('UpBwCurr', None)
        self.UpBwCurrUsage = kwargs.get('UpBwCurrUsage', None)
        self.DnBwCurr = kwargs.get('DnBwCurr', None)
        self.DnBwCurrUsage = kwargs.get('DnBwCurrUsage', None)
        self.TotBwCurr = kwargs.get('TotBwCurr', None)
        self.TotBwCurrUsage = kwargs.get('TotBwCurrUsage', None)
        self.CurrSessions = kwargs.get('CurrSessions', None)
        self.UpBwPeak = kwargs.get('UpBwPeak', None)
        self.UpBwPeakPer = kwargs.get('UpBwPeakPer', None)
        self.UpBwPeakTmSt = kwargs.get('UpBwPeakTmSt', None)
        self.DnBwPeak = kwargs.get('DnBwPeak', None)
        self.DnBwPeakPer = kwargs.get('DnBwPeakPer', None)
        self.DnBwPeakTmSt = kwargs.get('DnBwPeakTmSt', None)
        self.TotBwPeak = kwargs.get('TotBwPeak', None)
        self.TotBwPeakPer = kwargs.get('TotBwPeakPer', None)
        self.TotBwPeakTmSt = kwargs.get('TotBwPeakTmSt', None)
        self.LastClearTmSt = kwargs.get('LastClearTmSt', None)
        self.UpBwTot = kwargs.get('UpBwTot', None)
        self.DnBwTot = kwargs.get('DnBwTot', None)
        self.UpDnBwTot = kwargs.get('UpDnBwTot', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

