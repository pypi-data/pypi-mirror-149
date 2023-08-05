
from radware.sdk.beans_common import *


class EnumSpMemUseStatsProcOver1stMargin(BaseBeanEnum):
    over = 1
    below = 0


class EnumSpMemUseStatsProcOver2ndMargin(BaseBeanEnum):
    over = 1
    below = 0


class SpMemUseStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.InitProcessSize = kwargs.get('InitProcessSize', None)
        self.InitMaxProcessSize = kwargs.get('InitMaxProcessSize', None)
        self.InitSizeTo1Margin = kwargs.get('InitSizeTo1Margin', None)
        self.InitSizeTo2Margin = kwargs.get('InitSizeTo2Margin', None)
        self.AllowMemIncrease = kwargs.get('AllowMemIncrease', None)
        self.CurProcSize = kwargs.get('CurProcSize', None)
        self.CurProcShareSize = kwargs.get('CurProcShareSize', None)
        self.CurProcResidentSize = kwargs.get('CurProcResidentSize', None)
        self.CurFrontEndSessions = kwargs.get('CurFrontEndSessions', None)
        self.AvgFrontEndSessions = kwargs.get('AvgFrontEndSessions', None)
        self.PeakUsageFrom1stMargin = kwargs.get('PeakUsageFrom1stMargin', None)
        self.MemPressStat = kwargs.get('MemPressStat', None)
        self.MemUseFrom1stMargin = kwargs.get('MemUseFrom1stMargin', None)
        self.CurProcCacheRelativeSize = kwargs.get('CurProcCacheRelativeSize', None)
        self.CurProcDynCertRelativeSize = kwargs.get('CurProcDynCertRelativeSize', None)
        self.MemPressActiveTime = kwargs.get('MemPressActiveTime', None)
        self.MaxAllowConnections = kwargs.get('MaxAllowConnections', None)
        self.ProcOver1stMargin = EnumSpMemUseStatsProcOver1stMargin.enum(kwargs.get('ProcOver1stMargin', None))
        self.ProcOver2ndMargin = EnumSpMemUseStatsProcOver2ndMargin.enum(kwargs.get('ProcOver2ndMargin', None))
        self.MemTo2ndMargin = kwargs.get('MemTo2ndMargin', None)
        self.CurQatSlabsRelativeSize = kwargs.get('CurQatSlabsRelativeSize', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

