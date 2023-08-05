
from radware.sdk.beans_common import *


class EnumSlbWlmInfoState(BaseBeanEnum):
    connected = 1
    notconnected = 2


class SlbWlmInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.IpAddr = kwargs.get('IpAddr', None)
        self.Port = kwargs.get('Port', None)
        self.State = EnumSlbWlmInfoState.enum(kwargs.get('State', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

