
from radware.sdk.beans_common import *


class EnumSlbSmtportDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewCfgSmtportTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Num = kwargs.get('Num', None)
        self.Delete = EnumSlbSmtportDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

