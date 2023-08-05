
from radware.sdk.beans_common import *


class EnumDot1dTpFdbStatus(BaseBeanEnum):
    other = 1
    invalid = 2
    learned = 3
    self = 4
    mgmt = 5


class Dot1dTpFdbTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Address = kwargs.get('Address', None)
        self.Port = kwargs.get('Port', None)
        self.Status = EnumDot1dTpFdbStatus.enum(kwargs.get('Status', None))

    def get_indexes(self):
        return self.Address,
    
    @classmethod
    def get_index_names(cls):
        return 'Address',

