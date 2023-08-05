
from radware.sdk.beans_common import *


class EnumIntfInfoIpver(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumIntfInfoStatus(BaseBeanEnum):
    up = 1
    down = 2
    disabled = 3


class EnumIntfInfoBfd(BaseBeanEnum):
    on = 1
    off = 2


class IpIntfInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Ipver = EnumIntfInfoIpver.enum(kwargs.get('Ipver', None))
        self.Addr = kwargs.get('Addr', None)
        self.NetMask = kwargs.get('NetMask', None)
        self.BcastAddr = kwargs.get('BcastAddr', None)
        self.Vlan = kwargs.get('Vlan', None)
        self.Status = EnumIntfInfoStatus.enum(kwargs.get('Status', None))
        self.LinkLocalAddr = kwargs.get('LinkLocalAddr', None)
        self.Bfd = EnumIntfInfoBfd.enum(kwargs.get('Bfd', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

