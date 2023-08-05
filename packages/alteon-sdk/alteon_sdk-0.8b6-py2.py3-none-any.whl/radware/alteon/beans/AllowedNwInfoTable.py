
from radware.sdk.beans_common import *


class EnumAllowedNwInfoIpver(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class AllowedNwInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Ipver = EnumAllowedNwInfoIpver.enum(kwargs.get('Ipver', None))
        self.Vlan = kwargs.get('Vlan', None)
        self.BeginIpAddr = kwargs.get('BeginIpAddr', None)
        self.EndIpAddr = kwargs.get('EndIpAddr', None)
        self.NetMask = kwargs.get('NetMask', None)
        self.Ip6Prefix = kwargs.get('Ip6Prefix', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

