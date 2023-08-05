
from radware.sdk.beans_common import *


class EnumSlbWlmDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbWlmState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SlbNewCfgWlmTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.IpAddr = kwargs.get('IpAddr', None)
        self.Port = kwargs.get('Port', None)
        self.Delete = EnumSlbWlmDelete.enum(kwargs.get('Delete', None))
        self.Groups = kwargs.get('Groups', None)
        self.State = EnumSlbWlmState.enum(kwargs.get('State', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

