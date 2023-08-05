
from radware.sdk.beans_common import *


class EnumIpNwfState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumIpNwfDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumIpNwfIpVer(BaseBeanEnum):
    v4 = 0
    v6 = 1


class IpNewCfgNwfTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Addr = kwargs.get('Addr', None)
        self.Mask = kwargs.get('Mask', None)
        self.State = EnumIpNwfState.enum(kwargs.get('State', None))
        self.Delete = EnumIpNwfDelete.enum(kwargs.get('Delete', None))
        self.IpVer = EnumIpNwfIpVer.enum(kwargs.get('IpVer', None))
        self.Ipv6Addr = kwargs.get('Ipv6Addr', None)
        self.Ipv6Mask = kwargs.get('Ipv6Mask', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

