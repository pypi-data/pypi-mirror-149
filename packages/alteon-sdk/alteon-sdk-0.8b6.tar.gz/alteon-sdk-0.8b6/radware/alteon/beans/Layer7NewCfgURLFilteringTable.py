
from radware.sdk.beans_common import *


class EnumLayer7URLFilteringDelete(BaseBeanEnum):
    other = 1
    delete = 2


class Layer7NewCfgURLFilteringTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ID = kwargs.get('ID', None)
        self.Name = kwargs.get('Name', None)
        self.SecCatgs = kwargs.get('SecCatgs', None)
        self.CompCatgs = kwargs.get('CompCatgs', None)
        self.ProdCatgs = kwargs.get('ProdCatgs', None)
        self.Delete = EnumLayer7URLFilteringDelete.enum(kwargs.get('Delete', None))
        self.FallbackCatgs = kwargs.get('FallbackCatgs', None)

    def get_indexes(self):
        return self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ID',

