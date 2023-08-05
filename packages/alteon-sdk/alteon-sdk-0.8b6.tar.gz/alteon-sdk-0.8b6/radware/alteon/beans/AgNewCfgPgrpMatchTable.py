
from radware.sdk.beans_common import *


class EnumAgPgrpDelete(BaseBeanEnum):
    other = 1
    delete = 2


class AgNewCfgPgrpMatchTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Name = kwargs.get('Name', None)
        self.Add = kwargs.get('Add', None)
        self.Rem = kwargs.get('Rem', None)
        self.Bmap = kwargs.get('Bmap', None)
        self.Delete = EnumAgPgrpDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

