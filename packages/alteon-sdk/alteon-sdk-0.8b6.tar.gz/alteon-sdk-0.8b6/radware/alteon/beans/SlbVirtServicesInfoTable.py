
from radware.sdk.beans_common import *


class EnumSlbVirtServicesInfoState(BaseBeanEnum):
    blocked = 1
    running = 2
    failed = 3
    disabled = 4
    slowstart = 5
    overflow = 6
    noinstance = 7


class SlbVirtServicesInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VirtServIndex = kwargs.get('VirtServIndex', None)
        self.SvcIndex = kwargs.get('SvcIndex', None)
        self.RealServIndex = kwargs.get('RealServIndex', None)
        self.Vport = kwargs.get('Vport', None)
        self.Rport = kwargs.get('Rport', None)
        self.State = EnumSlbVirtServicesInfoState.enum(kwargs.get('State', None))
        self.ResponseTime = kwargs.get('ResponseTime', None)
        self.Weight = kwargs.get('Weight', None)
        self.CfgRealHealth = kwargs.get('CfgRealHealth', None)
        self.RtRealHealth = kwargs.get('RtRealHealth', None)
        self.StateFailReason = kwargs.get('StateFailReason', None)
        self.RealLogexp = kwargs.get('RealLogexp', None)

    def get_indexes(self):
        return self.VirtServIndex, self.SvcIndex, self.RealServIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'VirtServIndex', 'SvcIndex', 'RealServIndex',

