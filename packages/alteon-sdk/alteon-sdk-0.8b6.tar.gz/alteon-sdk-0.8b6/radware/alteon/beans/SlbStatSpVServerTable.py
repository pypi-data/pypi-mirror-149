
from radware.sdk.beans_common import *


class SlbStatSpVServerTable(DeviceBean):
    def __init__(self, **kwargs):
        self.SpIndex = kwargs.get('SpIndex', None)
        self.Index = kwargs.get('Index', None)
        self.CurrPSessions = kwargs.get('CurrPSessions', None)
        self.TotalPSessions = kwargs.get('TotalPSessions', None)
        self.HighestPSessions = kwargs.get('HighestPSessions', None)

    def get_indexes(self):
        return self.SpIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'SpIndex', 'Index',

