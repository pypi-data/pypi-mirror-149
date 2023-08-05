
from radware.sdk.beans_common import *


class EnumHaServiceTriggerCfgl4Reals(BaseBeanEnum):
    enabled = 1
    disabled = 2


class HaServiceTriggerNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Cfgl4Reals = EnumHaServiceTriggerCfgl4Reals.enum(kwargs.get('Cfgl4Reals', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

