
from radware.sdk.beans_common import *


class EnumPortStatsClear(BaseBeanEnum):
    ok = 1
    clear = 2


class PortStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.PhyIfInOctets = kwargs.get('PhyIfInOctets', None)
        self.PhyIfInUcastPkts = kwargs.get('PhyIfInUcastPkts', None)
        self.PhyIfInNUcastPkts = kwargs.get('PhyIfInNUcastPkts', None)
        self.PhyIfInDiscards = kwargs.get('PhyIfInDiscards', None)
        self.PhyIfInErrors = kwargs.get('PhyIfInErrors', None)
        self.PhyIfInUnknownProtos = kwargs.get('PhyIfInUnknownProtos', None)
        self.PhyIfOutOctets = kwargs.get('PhyIfOutOctets', None)
        self.PhyIfOutUcastPkts = kwargs.get('PhyIfOutUcastPkts', None)
        self.PhyIfOutNUcastPkts = kwargs.get('PhyIfOutNUcastPkts', None)
        self.PhyIfOutDiscards = kwargs.get('PhyIfOutDiscards', None)
        self.PhyIfOutErrors = kwargs.get('PhyIfOutErrors', None)
        self.PhyIfOutQLen = kwargs.get('PhyIfOutQLen', None)
        self.PhyIfInBroadcastPkts = kwargs.get('PhyIfInBroadcastPkts', None)
        self.PhyIfOutBroadcastPkts = kwargs.get('PhyIfOutBroadcastPkts', None)
        self.Clear = EnumPortStatsClear.enum(kwargs.get('Clear', None))
        self.PhyIfInMcastPkts = kwargs.get('PhyIfInMcastPkts', None)
        self.PhyIfOutMcastPkts = kwargs.get('PhyIfOutMcastPkts', None)

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

