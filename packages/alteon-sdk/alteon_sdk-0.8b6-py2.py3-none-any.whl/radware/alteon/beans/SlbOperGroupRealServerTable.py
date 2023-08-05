
from radware.sdk.beans_common import *


class EnumSlbOperGroupRealServerState(BaseBeanEnum):
    enable = 1
    disable = 2


class EnumSlbOperGroupRealServerStatus(BaseBeanEnum):
    enable = 1
    disable = 2


class SlbOperGroupRealServerTable(DeviceBean):
    def __init__(self, **kwargs):
        self.RealServGroupIndex = kwargs.get('RealServGroupIndex', None)
        self.ServIndex = kwargs.get('ServIndex', None)
        self.State = EnumSlbOperGroupRealServerState.enum(kwargs.get('State', None))
        self.Status = EnumSlbOperGroupRealServerStatus.enum(kwargs.get('Status', None))

    def get_indexes(self):
        return self.RealServGroupIndex, self.ServIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'RealServGroupIndex', 'ServIndex',

