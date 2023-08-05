
from radware.sdk.beans_common import *


class EnumIpv6StaticNbrAction(BaseBeanEnum):
    other = 1
    delete = 2


class Ipv6NewCfgStaticNbrTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.Ipv6Addr = kwargs.get('Ipv6Addr', None)
        self.MAC = kwargs.get('MAC', None)
        self.Vlan = kwargs.get('Vlan', None)
        self.Port = kwargs.get('Port', None)
        self.Action = EnumIpv6StaticNbrAction.enum(kwargs.get('Action', None))

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

