
from radware.sdk.beans_common import *


class EnumGslbInfoRemRealServerState(BaseBeanEnum):
    running = 2
    failed = 3
    disabled = 4


class GslbInfoRemRealServerTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Idx = kwargs.get('Idx', None)
        self.IpAddr = kwargs.get('IpAddr', None)
        self.Name = kwargs.get('Name', None)
        self.State = EnumGslbInfoRemRealServerState.enum(kwargs.get('State', None))

    def get_indexes(self):
        return self.Idx,
    
    @classmethod
    def get_index_names(cls):
        return 'Idx',

