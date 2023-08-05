
from radware.sdk.beans_common import *


class HaServiceTriggerIfsNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.NewCfgTrigIfTrackAdd = kwargs.get('NewCfgTrigIfTrackAdd', None)
        self.NewCfgTrigIfTrackExclude = kwargs.get('NewCfgTrigIfTrackExclude', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

