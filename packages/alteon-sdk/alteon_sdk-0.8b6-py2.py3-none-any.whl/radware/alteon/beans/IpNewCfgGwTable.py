
from radware.sdk.beans_common import *


class EnumIpGwState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumIpGwDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumIpGwArp(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumIpGwPriority(BaseBeanEnum):
    low = 1
    high = 2


class EnumIpGwIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class IpNewCfgGwTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Addr = kwargs.get('Addr', None)
        self.Interval = kwargs.get('Interval', None)
        self.Retry = kwargs.get('Retry', None)
        self.State = EnumIpGwState.enum(kwargs.get('State', None))
        self.Delete = EnumIpGwDelete.enum(kwargs.get('Delete', None))
        self.Arp = EnumIpGwArp.enum(kwargs.get('Arp', None))
        self.Vlan = kwargs.get('Vlan', None)
        self.Priority = EnumIpGwPriority.enum(kwargs.get('Priority', None))
        self.IpVer = EnumIpGwIpVer.enum(kwargs.get('IpVer', None))
        self.Ipv6Addr = kwargs.get('Ipv6Addr', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

