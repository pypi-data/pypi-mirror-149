
from radware.sdk.beans_common import *


class EnumHaServiceNewCfgTrigGwTrackState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class HaServiceTriggerGwNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.NewCfgTrigGwTrackState = EnumHaServiceNewCfgTrigGwTrackState.enum(kwargs.get('NewCfgTrigGwTrackState', None))
        self.NewCfgTrigGwTrackAdd = kwargs.get('NewCfgTrigGwTrackAdd', None)
        self.NewCfgTrigGwTrackExclude = kwargs.get('NewCfgTrigGwTrackExclude', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

