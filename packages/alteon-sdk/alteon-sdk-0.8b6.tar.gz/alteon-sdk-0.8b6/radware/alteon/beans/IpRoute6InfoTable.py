
from radware.sdk.beans_common import *


class EnumIpRoute6InfoProto(BaseBeanEnum):
    isis = 1
    rip = 2
    ospf = 3
    static = 4
    local = 5
    bgp = 6
    stlow = 7
    ospfi = 8
    ospfe = 9
    ospfe2 = 10
    ospfa = 11
    ripa = 12
    bgpa = 13
    igmp = 14
    unknown = 15
    natpt = 16


class IpRoute6InfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.DestIp6 = kwargs.get('DestIp6', None)
        self.Interface = kwargs.get('Interface', None)
        self.NextHop = kwargs.get('NextHop', None)
        self.Proto = EnumIpRoute6InfoProto.enum(kwargs.get('Proto', None))

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

