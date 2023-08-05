
from radware.sdk.beans_common import *


class EnumSlbOperRealServerStatus(BaseBeanEnum):
    enable = 1
    disable = 2
    cookiepersistent = 3
    fastage = 4
    cookiepersistentfastage = 5


class SlbOperRealServerTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Status = EnumSlbOperRealServerStatus.enum(kwargs.get('Status', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

