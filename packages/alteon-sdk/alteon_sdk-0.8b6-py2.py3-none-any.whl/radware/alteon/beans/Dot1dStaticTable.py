
from radware.sdk.beans_common import *


class EnumDot1dStaticStatus(BaseBeanEnum):
    other = 1
    invalid = 2
    permanent = 3
    deleteOnReset = 4
    deleteOnTimeout = 5


class Dot1dStaticTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Address = kwargs.get('Address', None)
        self.ReceivePort = kwargs.get('ReceivePort', None)
        self.AllowedToGoTo = kwargs.get('AllowedToGoTo', None)
        self.Status = EnumDot1dStaticStatus.enum(kwargs.get('Status', None))

    def get_indexes(self):
        return self.Address, self.ReceivePort,
    
    @classmethod
    def get_index_names(cls):
        return 'Address', 'ReceivePort',

