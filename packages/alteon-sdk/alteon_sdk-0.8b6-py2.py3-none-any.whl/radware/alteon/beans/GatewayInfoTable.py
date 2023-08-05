
from radware.sdk.beans_common import *


class EnumGatewayInfoStatus(BaseBeanEnum):
    up = 1
    failed = 2


class GatewayInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Addr = kwargs.get('Addr', None)
        self.Vlan = kwargs.get('Vlan', None)
        self.Status = EnumGatewayInfoStatus.enum(kwargs.get('Status', None))
        self.Addr6 = kwargs.get('Addr6', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

