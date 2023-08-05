
from radware.sdk.beans_common import *


class EnumSlbOperGroupRealServerState(BaseBeanEnum):
    enable = 1
    disable = 2
    shutdown_connection = 3
    shutdown_persistent_sessions = 4


class EnumSlbOperGroupRealServerStatus(BaseBeanEnum):
    enable = 1
    disable = 2
    shutdown_connection = 3
    shutdown_persistent_sessions = 4


class EnumSlbOperGroupRealServerRuntimeStatus(BaseBeanEnum):
    running = 1
    failed = 2
    disabled = 3
    overloaded = 4


class SlbOperEnhGroupRealServerTable(DeviceBean):
    def __init__(self, **kwargs):
        self.RealServGroupIndex = kwargs.get('RealServGroupIndex', None)
        self.ServIndex = kwargs.get('ServIndex', None)
        self.State = EnumSlbOperGroupRealServerState.enum(kwargs.get('State', None))
        self.Status = EnumSlbOperGroupRealServerStatus.enum(kwargs.get('Status', None))
        self.IP = kwargs.get('IP', None)
        self.Descr = kwargs.get('Descr', None)
        self.RuntimeStatus = EnumSlbOperGroupRealServerRuntimeStatus.enum(kwargs.get('RuntimeStatus', None))

    def get_indexes(self):
        return self.RealServGroupIndex, self.ServIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'RealServGroupIndex', 'ServIndex',

