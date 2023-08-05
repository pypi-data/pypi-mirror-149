
from radware.sdk.beans_common import *


class EnumIpAlistAction(BaseBeanEnum):
    permit = 1
    deny = 2


class EnumIpAlistState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumIpAlistDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumIpAlistNwType(BaseBeanEnum):
    network_filter = 1
    network_class = 2


class IpNewCfgAlistTable(DeviceBean):
    def __init__(self, **kwargs):
        self.RmapIndex = kwargs.get('RmapIndex', None)
        self.Index = kwargs.get('Index', None)
        self.Nwf = kwargs.get('Nwf', None)
        self.Metric = kwargs.get('Metric', None)
        self.Action = EnumIpAlistAction.enum(kwargs.get('Action', None))
        self.State = EnumIpAlistState.enum(kwargs.get('State', None))
        self.Delete = EnumIpAlistDelete.enum(kwargs.get('Delete', None))
        self.Nwc = kwargs.get('Nwc', None)
        self.NwType = EnumIpAlistNwType.enum(kwargs.get('NwType', None))

    def get_indexes(self):
        return self.RmapIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'RmapIndex', 'Index',

