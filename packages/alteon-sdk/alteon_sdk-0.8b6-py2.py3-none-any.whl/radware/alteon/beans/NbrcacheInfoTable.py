
from radware.sdk.beans_common import *


class EnumNbrcacheInfoState(BaseBeanEnum):
    undef = 1
    reach = 2
    stale = 3
    delay = 4
    probe = 5
    inval = 6
    unknown = 7
    incmp = 8


class EnumNbrcacheInfoType(BaseBeanEnum):
    undef = 1
    other = 2
    invalid = 3
    dynamic = 4
    static = 5
    local = 6


class NbrcacheInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.DestIp = kwargs.get('DestIp', None)
        self.State = EnumNbrcacheInfoState.enum(kwargs.get('State', None))
        self.Type = EnumNbrcacheInfoType.enum(kwargs.get('Type', None))
        self.MacAddr = kwargs.get('MacAddr', None)
        self.VlanId = kwargs.get('VlanId', None)
        self.PortNum = kwargs.get('PortNum', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

