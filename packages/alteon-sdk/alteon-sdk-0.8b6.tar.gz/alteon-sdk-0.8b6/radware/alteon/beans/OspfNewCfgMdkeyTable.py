
from radware.sdk.beans_common import *


class EnumOspfMdkeyDelete(BaseBeanEnum):
    other = 1
    delete = 2


class OspfNewCfgMdkeyTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Key = kwargs.get('Key', None)
        self.Delete = EnumOspfMdkeyDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

