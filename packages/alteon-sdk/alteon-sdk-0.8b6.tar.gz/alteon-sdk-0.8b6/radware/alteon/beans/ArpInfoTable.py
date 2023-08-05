
from radware.sdk.beans_common import *


class EnumArpInfoFlag(BaseBeanEnum):
    clear = 1
    unresolved = 2
    permanent = 3
    indirect = 4
    layer4 = 5


class ArpInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.DestIp = kwargs.get('DestIp', None)
        self.MacAddr = kwargs.get('MacAddr', None)
        self.VLAN = kwargs.get('VLAN', None)
        self.SrcPort = kwargs.get('SrcPort', None)
        self.RefPorts = kwargs.get('RefPorts', None)
        self.Flag = EnumArpInfoFlag.enum(kwargs.get('Flag', None))
        self.RefSPs = kwargs.get('RefSPs', None)

    def get_indexes(self):
        return self.DestIp,
    
    @classmethod
    def get_index_names(cls):
        return 'DestIp',

