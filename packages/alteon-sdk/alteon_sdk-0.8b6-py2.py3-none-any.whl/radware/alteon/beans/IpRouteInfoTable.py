
from radware.sdk.beans_common import *


class EnumIpRouteInfoTag(BaseBeanEnum):
    fixed = 1
    static = 2
    addr = 3
    rip = 4
    broadcast = 5
    martian = 6
    multicast = 7
    vip = 8
    bgp = 9
    ospf = 10
    none = 11


class EnumIpRouteInfoType(BaseBeanEnum):
    indirect = 1
    direct = 2
    local = 3
    broadcast = 4
    martian = 5
    multicast = 6
    other = 7


class IpRouteInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.DestIp = kwargs.get('DestIp', None)
        self.Mask = kwargs.get('Mask', None)
        self.Gateway = kwargs.get('Gateway', None)
        self.Tag = EnumIpRouteInfoTag.enum(kwargs.get('Tag', None))
        self.Type = EnumIpRouteInfoType.enum(kwargs.get('Type', None))
        self.Interface = kwargs.get('Interface', None)
        self.Gateway1 = kwargs.get('Gateway1', None)
        self.Gateway2 = kwargs.get('Gateway2', None)
        self.Metric = kwargs.get('Metric', None)

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

