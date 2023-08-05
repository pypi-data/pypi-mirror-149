
from radware.sdk.beans_common import *


class HaServiceTrackGwsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.TrackGwIndex = kwargs.get('TrackGwIndex', None)

    def get_indexes(self):
        return self.Index, self.TrackGwIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'Index', 'TrackGwIndex',

