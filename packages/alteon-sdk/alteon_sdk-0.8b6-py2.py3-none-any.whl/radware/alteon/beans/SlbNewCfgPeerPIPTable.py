
from radware.sdk.beans_common import *


class EnumSlbPeerPIPDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbPeerPIPVersion(BaseBeanEnum):
    unknown = 0
    ipv4 = 4
    ipv6 = 6


class SlbNewCfgPeerPIPTable(DeviceBean):
    def __init__(self, **kwargs):
        self.PIPIndex = kwargs.get('PIPIndex', None)
        self.PIPAddr = kwargs.get('PIPAddr', None)
        self.PIPv6Addr = kwargs.get('PIPv6Addr', None)
        self.PIPDelete = EnumSlbPeerPIPDelete.enum(kwargs.get('PIPDelete', None))
        self.PIPVersion = EnumSlbPeerPIPVersion.enum(kwargs.get('PIPVersion', None))

    def get_indexes(self):
        return self.PIPIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'PIPIndex',

