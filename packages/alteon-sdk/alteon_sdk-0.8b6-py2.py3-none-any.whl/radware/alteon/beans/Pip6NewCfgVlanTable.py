
from radware.sdk.beans_common import *


class EnumPip6VlanDelete(BaseBeanEnum):
    other = 1
    delete = 2


class Pip6NewCfgVlanTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Pip = kwargs.get('Pip', None)
        self.PipMap = kwargs.get('PipMap', None)
        self.Add = kwargs.get('Add', None)
        self.Remove = kwargs.get('Remove', None)
        self.Delete = EnumPip6VlanDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Pip,
    
    @classmethod
    def get_index_names(cls):
        return 'Pip',

