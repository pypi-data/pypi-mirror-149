
from radware.sdk.beans_common import *


class EnumAgAccessUserIdState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class AgAccessNewCfgEnhUserRealTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Serv = kwargs.get('Serv', None)
        self.IdState = EnumAgAccessUserIdState.enum(kwargs.get('IdState', None))

    def get_indexes(self):
        return self.Index, self.Serv,
    
    @classmethod
    def get_index_names(cls):
        return 'Index', 'Serv',

