
from radware.sdk.beans_common import *


class EnumIpStaticArpAction(BaseBeanEnum):
    other = 1
    delete = 2


class IpNewCfgStaticArpTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.Ip = kwargs.get('Ip', None)
        self.MAC = kwargs.get('MAC', None)
        self.Vlan = kwargs.get('Vlan', None)
        self.Port = kwargs.get('Port', None)
        self.Action = EnumIpStaticArpAction.enum(kwargs.get('Action', None))

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

