
from radware.sdk.beans_common import *


class EnumFltHttpRedirMappingDelete(BaseBeanEnum):
    other = 1
    delete = 2


class FltNewCfgHttpRedirMappingTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Filter = kwargs.get('Filter', None)
        self.FromStr = kwargs.get('FromStr', None)
        self.ToStr = kwargs.get('ToStr', None)
        self.Delete = EnumFltHttpRedirMappingDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Filter, self.FromStr,
    
    @classmethod
    def get_index_names(cls):
        return 'Filter', 'FromStr',

