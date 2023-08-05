
from radware.sdk.beans_common import *


class GslbStatEnhNetworkTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Idx = kwargs.get('Idx', None)
        self.Hit = kwargs.get('Hit', None)
        self.IpAddr = kwargs.get('IpAddr', None)
        self.Ipv6Addr = kwargs.get('Ipv6Addr', None)
        self.SrcType = kwargs.get('SrcType', None)
        self.ClassId = kwargs.get('ClassId', None)

    def get_indexes(self):
        return self.Idx,
    
    @classmethod
    def get_index_names(cls):
        return 'Idx',

