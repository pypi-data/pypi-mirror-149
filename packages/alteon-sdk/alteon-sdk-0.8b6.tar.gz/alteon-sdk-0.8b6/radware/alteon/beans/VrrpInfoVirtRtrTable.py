
from radware.sdk.beans_common import *


class EnumVrrpInfoVirtRtrState(BaseBeanEnum):
    init = 1
    master = 2
    backup = 3
    holdoff = 4


class EnumVrrpInfoVirtRtrOwnership(BaseBeanEnum):
    owner = 1
    renter = 2


class EnumVrrpInfoVirtRtrServer(BaseBeanEnum):
    yes = 1
    no = 2


class EnumVrrpInfoVirtRtrProxy(BaseBeanEnum):
    yes = 1
    no = 2


class VrrpInfoVirtRtrTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.State = EnumVrrpInfoVirtRtrState.enum(kwargs.get('State', None))
        self.Ownership = EnumVrrpInfoVirtRtrOwnership.enum(kwargs.get('Ownership', None))
        self.Server = EnumVrrpInfoVirtRtrServer.enum(kwargs.get('Server', None))
        self.Proxy = EnumVrrpInfoVirtRtrProxy.enum(kwargs.get('Proxy', None))
        self.Priority = kwargs.get('Priority', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

