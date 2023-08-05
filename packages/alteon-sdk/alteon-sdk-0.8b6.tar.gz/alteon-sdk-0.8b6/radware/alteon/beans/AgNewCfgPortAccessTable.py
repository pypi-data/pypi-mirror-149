
from radware.sdk.beans_common import *


class EnumAgPortAccessState(BaseBeanEnum):
    deny = 0
    allow = 1


class AgNewCfgPortAccessTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.State = EnumAgPortAccessState.enum(kwargs.get('State', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

