
from radware.sdk.beans_common import *


class HaServiceTrackIfsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.TrackIfIndex = kwargs.get('TrackIfIndex', None)

    def get_indexes(self):
        return self.Index, self.TrackIfIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'Index', 'TrackIfIndex',

