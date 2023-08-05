
from radware.sdk.beans_common import *


class EnumPortTeamState(BaseBeanEnum):
    enable = 1
    disable = 2


class EnumPortTeamDelete(BaseBeanEnum):
    other = 1
    delete = 2


class PortTeamNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.State = EnumPortTeamState.enum(kwargs.get('State', None))
        self.Ports = kwargs.get('Ports', None)
        self.AddPort = kwargs.get('AddPort', None)
        self.RemovePort = kwargs.get('RemovePort', None)
        self.Trunks = kwargs.get('Trunks', None)
        self.AddTrunk = kwargs.get('AddTrunk', None)
        self.RemoveTrunk = kwargs.get('RemoveTrunk', None)
        self.Delete = EnumPortTeamDelete.enum(kwargs.get('Delete', None))
        self.Name = kwargs.get('Name', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

