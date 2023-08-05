
from radware.sdk.beans_common import *


class EnumBgpAggrState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumBgpAggrDelete(BaseBeanEnum):
    other = 1
    delete = 2


class BgpNewCfgAggrTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Addr = kwargs.get('Addr', None)
        self.Mask = kwargs.get('Mask', None)
        self.State = EnumBgpAggrState.enum(kwargs.get('State', None))
        self.Delete = EnumBgpAggrDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

