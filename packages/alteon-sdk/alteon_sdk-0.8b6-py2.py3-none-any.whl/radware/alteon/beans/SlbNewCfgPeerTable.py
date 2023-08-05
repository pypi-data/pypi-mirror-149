
from radware.sdk.beans_common import *


class EnumSlbPeerState(BaseBeanEnum):
    enable = 1
    disable = 2


class EnumSlbPeerDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbPeerIpVersion(BaseBeanEnum):
    ipv4 = 4
    ipv6 = 6


class SlbNewCfgPeerTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.IpAddr = kwargs.get('IpAddr', None)
        self.State = EnumSlbPeerState.enum(kwargs.get('State', None))
        self.Delete = EnumSlbPeerDelete.enum(kwargs.get('Delete', None))
        self.Ipv6Addr = kwargs.get('Ipv6Addr', None)
        self.IpVersion = EnumSlbPeerIpVersion.enum(kwargs.get('IpVersion', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

