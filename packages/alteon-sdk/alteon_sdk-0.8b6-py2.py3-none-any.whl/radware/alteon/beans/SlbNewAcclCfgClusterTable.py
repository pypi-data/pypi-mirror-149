
from radware.sdk.beans_common import *


class EnumSlbAcclClusterAdminStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclClusterDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewAcclCfgClusterTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VirtId = kwargs.get('VirtId', None)
        self.ServiceVport = kwargs.get('ServiceVport', None)
        self.AdminStatus = EnumSlbAcclClusterAdminStatus.enum(kwargs.get('AdminStatus', None))
        self.PeerVIP1 = kwargs.get('PeerVIP1', None)
        self.PeerVIP2 = kwargs.get('PeerVIP2', None)
        self.PeerVIP3 = kwargs.get('PeerVIP3', None)
        self.PeerVIP4 = kwargs.get('PeerVIP4', None)
        self.PeerVIP5 = kwargs.get('PeerVIP5', None)
        self.Delete = EnumSlbAcclClusterDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.VirtId, self.ServiceVport,
    
    @classmethod
    def get_index_names(cls):
        return 'VirtId', 'ServiceVport',

