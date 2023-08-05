
from radware.sdk.beans_common import *


class EnumPortTeamInfoState(BaseBeanEnum):
    off = 1
    passive = 2
    active = 3


class PortTeamInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.State = EnumPortTeamInfoState.enum(kwargs.get('State', None))
        self.Ports = kwargs.get('Ports', None)
        self.PortsState = kwargs.get('PortsState', None)
        self.Trunks = kwargs.get('Trunks', None)
        self.TrunksState = kwargs.get('TrunksState', None)
        self.Master = kwargs.get('Master', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

