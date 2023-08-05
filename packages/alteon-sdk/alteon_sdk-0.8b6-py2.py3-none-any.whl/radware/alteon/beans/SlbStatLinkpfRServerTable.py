
from radware.sdk.beans_common import *


class EnumSlbStatLinkpfRServerState(BaseBeanEnum):
    running = 1
    failed = 2
    disabled = 3


class SlbStatLinkpfRServerTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.IpAddr = kwargs.get('IpAddr', None)
        self.UpBwCurr = kwargs.get('UpBwCurr', None)
        self.UpBwUsage = kwargs.get('UpBwUsage', None)
        self.DwBwCurr = kwargs.get('DwBwCurr', None)
        self.DwBwUSage = kwargs.get('DwBwUSage', None)
        self.TotCurrbw = kwargs.get('TotCurrbw', None)
        self.TotCurrUsage = kwargs.get('TotCurrUsage', None)
        self.CurrSess = kwargs.get('CurrSess', None)
        self.UpBwPeak = kwargs.get('UpBwPeak', None)
        self.UpBwPeakPer = kwargs.get('UpBwPeakPer', None)
        self.UpBwPeakTmSt = kwargs.get('UpBwPeakTmSt', None)
        self.DnBwPeak = kwargs.get('DnBwPeak', None)
        self.DnBwPeakPer = kwargs.get('DnBwPeakPer', None)
        self.DnBwPeakTmSt = kwargs.get('DnBwPeakTmSt', None)
        self.TotBwPeak = kwargs.get('TotBwPeak', None)
        self.TotBwPeakPer = kwargs.get('TotBwPeakPer', None)
        self.TotBwPeakTmSt = kwargs.get('TotBwPeakTmSt', None)
        self.LastTranfetTmSt = kwargs.get('LastTranfetTmSt', None)
        self.UpBwTot = kwargs.get('UpBwTot', None)
        self.DnBwTot = kwargs.get('DnBwTot', None)
        self.UpDnBwTot = kwargs.get('UpDnBwTot', None)
        self.State = EnumSlbStatLinkpfRServerState.enum(kwargs.get('State', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

