
from radware.sdk.beans_common import *


class EnumPip6Delete(BaseBeanEnum):
    other = 1
    delete = 2


class Pip6NewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Pip = kwargs.get('Pip', None)
        self.PortMap = kwargs.get('PortMap', None)
        self.VlanMap = kwargs.get('VlanMap', None)
        self.Delete = EnumPip6Delete.enum(kwargs.get('Delete', None))
        self.AddPortVlan = kwargs.get('AddPortVlan', None)
        self.RemovePortVlan = kwargs.get('RemovePortVlan', None)
        self.AddPort = kwargs.get('AddPort', None)
        self.AddVlan = kwargs.get('AddVlan', None)
        self.RemovePort = kwargs.get('RemovePort', None)
        self.RemoveVlan = kwargs.get('RemoveVlan', None)

    def get_indexes(self):
        return self.Pip,
    
    @classmethod
    def get_index_names(cls):
        return 'Pip',

