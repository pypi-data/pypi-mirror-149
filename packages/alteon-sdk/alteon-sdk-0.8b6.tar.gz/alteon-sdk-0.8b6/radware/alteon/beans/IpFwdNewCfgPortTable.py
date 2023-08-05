
from radware.sdk.beans_common import *


class EnumIpFwdPortState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class IpFwdNewCfgPortTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.State = EnumIpFwdPortState.enum(kwargs.get('State', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

