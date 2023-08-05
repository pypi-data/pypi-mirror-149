
from radware.sdk.beans_common import *


class EnumIpIntfState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumIpIntfDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumIpIntfBootpRelay(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumIpIntfIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumIpIntfRouteAdv(BaseBeanEnum):
    enabled = 1
    disabled = 2


class IpNewCfgIntfTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Addr = kwargs.get('Addr', None)
        self.Mask = kwargs.get('Mask', None)
        self.Vlan = kwargs.get('Vlan', None)
        self.State = EnumIpIntfState.enum(kwargs.get('State', None))
        self.Delete = EnumIpIntfDelete.enum(kwargs.get('Delete', None))
        self.BootpRelay = EnumIpIntfBootpRelay.enum(kwargs.get('BootpRelay', None))
        self.IpVer = EnumIpIntfIpVer.enum(kwargs.get('IpVer', None))
        self.Ipv6Addr = kwargs.get('Ipv6Addr', None)
        self.PrefixLen = kwargs.get('PrefixLen', None)
        self.RouteAdv = EnumIpIntfRouteAdv.enum(kwargs.get('RouteAdv', None))
        self.Peer = kwargs.get('Peer', None)
        self.Description = kwargs.get('Description', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

