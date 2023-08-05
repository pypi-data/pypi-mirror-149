
from radware.sdk.beans_common import *


class EnumIpv6StaticRouteAction(BaseBeanEnum):
    other = 1
    delete = 2


class Ipv6NewCfgStaticRouteTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.DestIp = kwargs.get('DestIp', None)
        self.Mask = kwargs.get('Mask', None)
        self.Gateway = kwargs.get('Gateway', None)
        self.Action = EnumIpv6StaticRouteAction.enum(kwargs.get('Action', None))
        self.Vlan = kwargs.get('Vlan', None)

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

