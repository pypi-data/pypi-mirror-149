
from radware.sdk.beans_common import *


class EnumHaServiceNewCfgTrigRealTrkState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumHaServiceNewCfgTrigAllRemRealState(BaseBeanEnum):
    aadd = 1
    arem = 2


class EnumHaServiceNewCfgTrigRealTrkAutoOptState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class HaServiceTriggerRealNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.NewCfgTrigRealTrkState = EnumHaServiceNewCfgTrigRealTrkState.enum(kwargs.get('NewCfgTrigRealTrkState', None))
        self.NewCfgTrigAllRemRealState = EnumHaServiceNewCfgTrigAllRemRealState.enum(kwargs.get('NewCfgTrigAllRemRealState', None))
        self.NewCfgTrigAddReals = kwargs.get('NewCfgTrigAddReals', None)
        self.NewCfgTrigRemReals = kwargs.get('NewCfgTrigRemReals', None)
        self.NewCfgTrigRealTrkAutoOptState = EnumHaServiceNewCfgTrigRealTrkAutoOptState.enum(kwargs.get('NewCfgTrigRealTrkAutoOptState', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

