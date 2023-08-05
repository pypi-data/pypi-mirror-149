
from radware.sdk.beans_common import *


class EnumIpAspathAction(BaseBeanEnum):
    permit = 1
    deny = 2


class EnumIpAspathState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumIpAspathDelete(BaseBeanEnum):
    other = 1
    delete = 2


class IpNewCfgAspathTable(DeviceBean):
    def __init__(self, **kwargs):
        self.RmapIndex = kwargs.get('RmapIndex', None)
        self.Index = kwargs.get('Index', None)
        self.AS = kwargs.get('AS', None)
        self.Action = EnumIpAspathAction.enum(kwargs.get('Action', None))
        self.State = EnumIpAspathState.enum(kwargs.get('State', None))
        self.Delete = EnumIpAspathDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.RmapIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'RmapIndex', 'Index',

