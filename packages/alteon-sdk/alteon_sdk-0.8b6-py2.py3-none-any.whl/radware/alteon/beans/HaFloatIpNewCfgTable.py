
from radware.sdk.beans_common import *


class EnumHaFloatIpIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumHaFloatIpDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumHaFloatIpState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class HaFloatIpNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.IpVer = EnumHaFloatIpIpVer.enum(kwargs.get('IpVer', None))
        self.IpAddr = kwargs.get('IpAddr', None)
        self.Ipv6Addr = kwargs.get('Ipv6Addr', None)
        self.If = kwargs.get('If', None)
        self.Delete = EnumHaFloatIpDelete.enum(kwargs.get('Delete', None))
        self.State = EnumHaFloatIpState.enum(kwargs.get('State', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

