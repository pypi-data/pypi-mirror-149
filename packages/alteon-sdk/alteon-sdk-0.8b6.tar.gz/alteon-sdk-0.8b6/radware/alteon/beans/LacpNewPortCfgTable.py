
from radware.sdk.beans_common import *


class EnumLacpPortState(BaseBeanEnum):
    off = 1
    active = 2
    passive = 3


class LacpNewPortCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Id = kwargs.get('Id', None)
        self.State = EnumLacpPortState.enum(kwargs.get('State', None))
        self.ActorPortPriority = kwargs.get('ActorPortPriority', None)
        self.ActorAdminKey = kwargs.get('ActorAdminKey', None)

    def get_indexes(self):
        return self.Id,
    
    @classmethod
    def get_index_names(cls):
        return 'Id',

