
from radware.sdk.beans_common import *


class EnumGslbLocalDnsDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumGslbLocalDnsVersion(BaseBeanEnum):
    unknown = 0
    ipv4 = 4
    ipv6 = 6


class GslbNewCfgLocalDnsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Addr = kwargs.get('Addr', None)
        self.Dnsv6Addr = kwargs.get('Dnsv6Addr', None)
        self.Delete = EnumGslbLocalDnsDelete.enum(kwargs.get('Delete', None))
        self.Version = EnumGslbLocalDnsVersion.enum(kwargs.get('Version', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

