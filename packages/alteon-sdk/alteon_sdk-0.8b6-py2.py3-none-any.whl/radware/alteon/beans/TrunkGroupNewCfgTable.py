
from radware.sdk.beans_common import *


class EnumTrunkGroupState(BaseBeanEnum):
    enable = 1
    disable = 2


class EnumTrunkGroupDelete(BaseBeanEnum):
    other = 1
    delete = 2


class TrunkGroupNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Ports = kwargs.get('Ports', None)
        self.AddPort = kwargs.get('AddPort', None)
        self.RemovePort = kwargs.get('RemovePort', None)
        self.State = EnumTrunkGroupState.enum(kwargs.get('State', None))
        self.Delete = EnumTrunkGroupDelete.enum(kwargs.get('Delete', None))
        self.BwmContract = kwargs.get('BwmContract', None)
        self.Name = kwargs.get('Name', None)
        self.PortCount = kwargs.get('PortCount', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

