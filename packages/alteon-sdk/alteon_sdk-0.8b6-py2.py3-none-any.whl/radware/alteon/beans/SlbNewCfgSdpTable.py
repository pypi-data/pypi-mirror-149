
from radware.sdk.beans_common import *


class EnumSlbSdpDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewCfgSdpTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.PrivAddr = kwargs.get('PrivAddr', None)
        self.PublicAddr = kwargs.get('PublicAddr', None)
        self.Delete = EnumSlbSdpDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

