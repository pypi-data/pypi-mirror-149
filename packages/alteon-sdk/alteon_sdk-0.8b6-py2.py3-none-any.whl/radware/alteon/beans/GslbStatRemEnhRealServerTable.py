
from radware.sdk.beans_common import *


class EnumGslbStatRemRealServerIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class GslbStatRemEnhRealServerTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.DnsHandoffs = kwargs.get('DnsHandoffs', None)
        self.HttpRedirs = kwargs.get('HttpRedirs', None)
        self.ThresholdExceeded = kwargs.get('ThresholdExceeded', None)
        self.IpAddress = kwargs.get('IpAddress', None)
        self.Ipv6Address = kwargs.get('Ipv6Address', None)
        self.IpVer = EnumGslbStatRemRealServerIpVer.enum(kwargs.get('IpVer', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

