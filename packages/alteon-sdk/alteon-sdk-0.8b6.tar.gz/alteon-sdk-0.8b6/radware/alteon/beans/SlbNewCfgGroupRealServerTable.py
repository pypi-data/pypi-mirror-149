
from radware.sdk.beans_common import *


class EnumSlbGroupRealServerState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SlbNewCfgGroupRealServerTable(DeviceBean):
    def __init__(self, **kwargs):
        self.RealServGroupIndex = kwargs.get('RealServGroupIndex', None)
        self.ServIndex = kwargs.get('ServIndex', None)
        self.State = EnumSlbGroupRealServerState.enum(kwargs.get('State', None))

    def get_indexes(self):
        return self.RealServGroupIndex, self.ServIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'RealServGroupIndex', 'ServIndex',

