
from radware.sdk.beans_common import *


class EnumAgVLANAccessState(BaseBeanEnum):
    deny = 0
    allow = 1


class AgNewCfgVLANAccessTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.State = EnumAgVLANAccessState.enum(kwargs.get('State', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

