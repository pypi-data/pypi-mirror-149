
from radware.sdk.beans_common import *


class EnumSpMaintStatsClear(BaseBeanEnum):
    ok = 1
    clear = 2


class SpMaintStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.SpIndex = kwargs.get('SpIndex', None)
        self.PfdbFreeEmpty = kwargs.get('PfdbFreeEmpty', None)
        self.ResolveErrNoddw = kwargs.get('ResolveErrNoddw', None)
        self.LearnErrNoddw = kwargs.get('LearnErrNoddw', None)
        self.AgeMPNoddw = kwargs.get('AgeMPNoddw', None)
        self.DeleteMiss = kwargs.get('DeleteMiss', None)
        self.RecvLetErrorsMP = kwargs.get('RecvLetErrorsMP', None)
        self.RecvLetErrorsSP1 = kwargs.get('RecvLetErrorsSP1', None)
        self.RecvLetErrorsSP2 = kwargs.get('RecvLetErrorsSP2', None)
        self.RecvLetErrorsSP3 = kwargs.get('RecvLetErrorsSP3', None)
        self.RecvLetErrorsSP4 = kwargs.get('RecvLetErrorsSP4', None)
        self.SendLetFailsMP = kwargs.get('SendLetFailsMP', None)
        self.SendLetFailsSP1 = kwargs.get('SendLetFailsSP1', None)
        self.SendLetFailsSP2 = kwargs.get('SendLetFailsSP2', None)
        self.SendLetFailsSP3 = kwargs.get('SendLetFailsSP3', None)
        self.SendLetFailsSP4 = kwargs.get('SendLetFailsSP4', None)
        self.RecvLetSuccessMP = kwargs.get('RecvLetSuccessMP', None)
        self.RecvLetSuccessSP1 = kwargs.get('RecvLetSuccessSP1', None)
        self.RecvLetSuccessSP2 = kwargs.get('RecvLetSuccessSP2', None)
        self.RecvLetSuccessSP3 = kwargs.get('RecvLetSuccessSP3', None)
        self.RecvLetSuccessSP4 = kwargs.get('RecvLetSuccessSP4', None)
        self.SendLetSuccessMP = kwargs.get('SendLetSuccessMP', None)
        self.SendLetSuccessSP1 = kwargs.get('SendLetSuccessSP1', None)
        self.SendLetSuccessSP2 = kwargs.get('SendLetSuccessSP2', None)
        self.SendLetSuccessSP3 = kwargs.get('SendLetSuccessSP3', None)
        self.SendLetSuccessSP4 = kwargs.get('SendLetSuccessSP4', None)
        self.RateLimitArpDrops = kwargs.get('RateLimitArpDrops', None)
        self.RateLimitIcmpDrops = kwargs.get('RateLimitIcmpDrops', None)
        self.RateLimitTcpDrops = kwargs.get('RateLimitTcpDrops', None)
        self.RateLimitUdpDrops = kwargs.get('RateLimitUdpDrops', None)
        self.RecvLetErrorsSP5 = kwargs.get('RecvLetErrorsSP5', None)
        self.RecvLetErrorsSP6 = kwargs.get('RecvLetErrorsSP6', None)
        self.RecvLetErrorsSP7 = kwargs.get('RecvLetErrorsSP7', None)
        self.SendLetFailsSP5 = kwargs.get('SendLetFailsSP5', None)
        self.SendLetFailsSP6 = kwargs.get('SendLetFailsSP6', None)
        self.SendLetFailsSP7 = kwargs.get('SendLetFailsSP7', None)
        self.RecvLetSuccessSP5 = kwargs.get('RecvLetSuccessSP5', None)
        self.RecvLetSuccessSP6 = kwargs.get('RecvLetSuccessSP6', None)
        self.RecvLetSuccessSP7 = kwargs.get('RecvLetSuccessSP7', None)
        self.SendLetSuccessSP5 = kwargs.get('SendLetSuccessSP5', None)
        self.SendLetSuccessSP6 = kwargs.get('SendLetSuccessSP6', None)
        self.SendLetSuccessSP7 = kwargs.get('SendLetSuccessSP7', None)
        self.Clear = EnumSpMaintStatsClear.enum(kwargs.get('Clear', None))

    def get_indexes(self):
        return self.SpIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'SpIndex',

