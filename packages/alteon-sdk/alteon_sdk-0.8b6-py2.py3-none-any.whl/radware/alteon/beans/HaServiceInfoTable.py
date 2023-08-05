
from radware.sdk.beans_common import *


class EnumHaServiceInfoState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class HaServiceInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.State = EnumHaServiceInfoState.enum(kwargs.get('State', None))
        self.GroupInfoState = kwargs.get('GroupInfoState', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

