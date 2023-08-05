
from radware.sdk.beans_common import *


class EnumSlbRealServerRportInfoState(BaseBeanEnum):
    up = 1
    down = 2
    slowstart = 3


class SlbEnhRealServerRportInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.RealIndex = kwargs.get('RealIndex', None)
        self.ServIndex = kwargs.get('ServIndex', None)
        self.Rport = kwargs.get('Rport', None)
        self.State = EnumSlbRealServerRportInfoState.enum(kwargs.get('State', None))
        self.Group = kwargs.get('Group', None)
        self.RespTime = kwargs.get('RespTime', None)
        self.FailReason = kwargs.get('FailReason', None)

    def get_indexes(self):
        return self.RealIndex, self.ServIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'RealIndex', 'ServIndex',

