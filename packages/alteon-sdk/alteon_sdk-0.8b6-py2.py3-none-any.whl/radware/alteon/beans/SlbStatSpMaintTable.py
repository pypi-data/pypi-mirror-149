
from radware.sdk.beans_common import *


class EnumSlbStatSpMaintClear(BaseBeanEnum):
    ok = 1
    clear = 2


class SlbStatSpMaintTable(DeviceBean):
    def __init__(self, **kwargs):
        self.SpIndex = kwargs.get('SpIndex', None)
        self.MaximumSessions = kwargs.get('MaximumSessions', None)
        self.CurBindings = kwargs.get('CurBindings', None)
        self.CurBindings4Seconds = kwargs.get('CurBindings4Seconds', None)
        self.CurBindings64Seconds = kwargs.get('CurBindings64Seconds', None)
        self.TerminatedSessions = kwargs.get('TerminatedSessions', None)
        self.BindingFails = kwargs.get('BindingFails', None)
        self.NonTcpFrames = kwargs.get('NonTcpFrames', None)
        self.UdpDatagrams = kwargs.get('UdpDatagrams', None)
        self.IncorrectVIPs = kwargs.get('IncorrectVIPs', None)
        self.IncorrectVports = kwargs.get('IncorrectVports', None)
        self.RealServerNoAvails = kwargs.get('RealServerNoAvails', None)
        self.FilteredDeniedFrames = kwargs.get('FilteredDeniedFrames', None)
        self.LandAttacks = kwargs.get('LandAttacks', None)
        self.IpFragTotalSessions = kwargs.get('IpFragTotalSessions', None)
        self.IpFragCurSessions = kwargs.get('IpFragCurSessions', None)
        self.IpFragDiscards = kwargs.get('IpFragDiscards', None)
        self.IpFragTableFull = kwargs.get('IpFragTableFull', None)
        self.Clear = EnumSlbStatSpMaintClear.enum(kwargs.get('Clear', None))
        self.OOSFinPktDrops = kwargs.get('OOSFinPktDrops', None)
        self.SymSessions = kwargs.get('SymSessions', None)
        self.SymValidSegments = kwargs.get('SymValidSegments', None)
        self.SymFragSessions = kwargs.get('SymFragSessions', None)
        self.SymSegAllocFails = kwargs.get('SymSegAllocFails', None)
        self.SymBufferAllocFails = kwargs.get('SymBufferAllocFails', None)
        self.SymConnAllocFails = kwargs.get('SymConnAllocFails', None)
        self.SymInvalidBuffers = kwargs.get('SymInvalidBuffers', None)
        self.SymSegReallocFails = kwargs.get('SymSegReallocFails', None)
        self.SymPacketsIn = kwargs.get('SymPacketsIn', None)
        self.SymPacketsWithNoData = kwargs.get('SymPacketsWithNoData', None)
        self.SymTcpPackets = kwargs.get('SymTcpPackets', None)
        self.SymUdpPackets = kwargs.get('SymUdpPackets', None)
        self.SymIcmpPackets = kwargs.get('SymIcmpPackets', None)
        self.SymOtherPackets = kwargs.get('SymOtherPackets', None)
        self.SymMatchCount = kwargs.get('SymMatchCount', None)
        self.SymFetchErrors = kwargs.get('SymFetchErrors', None)
        self.SymTruncPayloadToMp = kwargs.get('SymTruncPayloadToMp', None)
        self.SymPacketsInFastPath = kwargs.get('SymPacketsInFastPath', None)
        self.PeakBindings = kwargs.get('PeakBindings', None)
        self.CurAxBindings = kwargs.get('CurAxBindings', None)
        self.CurAxBindings4Seconds = kwargs.get('CurAxBindings4Seconds', None)
        self.CurAxBindings64Seconds = kwargs.get('CurAxBindings64Seconds', None)
        self.PeakAxBindings = kwargs.get('PeakAxBindings', None)

    def get_indexes(self):
        return self.SpIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'SpIndex',

